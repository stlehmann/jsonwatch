#!/usr/bin/env python
"""
    watcher.py Copyright (c) 2015 by stefanlehmann
    
"""

import serial
import threading
import queue
import curses
from jsonwatch import JsonNode, JsonItem


COMPORT = "/dev/cu.usbmodemfa131"
bytestostr = lambda x: x.decode('utf-8')
strtobytes = lambda x: bytearray(x, 'utf-8')


def read_serial(ser: serial.Serial, q_out: queue.Queue, q_in: queue.Queue):
    while (ser.isOpen()):
        if not q_in.empty():
            ser.write(q_in.get() + b'\n')
        q_out.put(bytestostr(ser.readline()))



def open_serial(port):
    ser = serial.Serial(port)
    ser.setBaudrate(9600)
    return ser


def main(stdscr):
    ser = open_serial(COMPORT)
    q_receive = queue.Queue()
    q_send = queue.Queue()
    root = JsonNode('root')

    worker = threading.Thread(target=read_serial, args=(ser, q_receive, q_send))
    worker.start()

    curses.echo()
    stdscr.nodelay(True)
    stdscr.clear()

    y = 0
    try:
        while True:
            if not q_receive.empty():
                s = q_receive.get()
                root.values_from_json(s)
                y, x = iter_print(root, stdscr, 0, 0)

            try:
                char = stdscr.getkey(y+1, 0)
                stdscr.nodelay(False)
                s = bytes(char, 'utf-8') + stdscr.getstr()
                q_send.put(s)
                stdscr.move(y+1, 0)
                stdscr.deleteln()
                stdscr.nodelay(True)
            except curses.error:
                pass

    except KeyboardInterrupt:
        ser.close()

def iter_print(node, scr, y, x):
    scr.addstr(y, x, "%s" % node.key)
    y += 1
    x += 2
    for child in node.items:
        if isinstance(child, JsonNode):
            y, x_ = iter_print(child, scr, y, x)
        else:
            scr.addstr(y, x, "%s: %s" % (child.key, str(child.value)))
            y += 1
    return y, x

curses.wrapper(main)