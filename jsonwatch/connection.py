#!-*- coding: utf-8 -*-
"""
Module for diffent connections.

:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com

"""
import blinker
import logging
import threading
from serial import Serial
import socket


logger = logging.getLogger(__name__)


class Connection:
    pass


class SerialConnection(Connection):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.serial = Serial(*args, **kwargs)

    def open(self):
        self.serial.open()

    def close(self):
        self.serial.close()

    def send(self, data):
        return self.serial.write(data)

    def receive(self, size=1):
        return self.serial.read(size)

    @property
    def connected(self):
        return self.serial.is_open()


class SocketConnection(Connection):
    def __init__(self, address=None):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False
        if address:
            self.open(address[0], address[1])

    def open(self, host=None, port=None):
        self.socket.connect((host, port))
        self._connected = True

    def close(self):
        self.socket.close()
        self._connected = False

    def send(self, data: bytes):
        return self.socket.send(bytes)

    def receive(self):
        return self.socket.recv(4096)

    @property
    def connected(self):
        return self._connected


class ConnectionThread(threading.Thread):
    def __init__(self, connection, *args, **kwargs):
        self.connection = connection
        self._run = True

        # buffer for incoming bytes
        self._buffer = ''

        # message buffer
        self._messages = []

        # clear messages after read
        self._clear_messages = False

        # blinker signal for received data
        self.new_messages = blinker.signal('new_messages')

        super(ConnectionThread, self).__init__(*args, **kwargs)

    def run(self):
        while self._run:
            # clear messages after last read
            if self._clear_messages:
                self._messages.clear()
                self._clear_messages = False

            new_data = self.connection.receive()
            self._buffer += new_data.decode()
            messages = self._buffer.split('\n')
            while len(messages) > 1:
                message = messages.pop(0)
                self._messages.append(message)
                self.new_messages.send(self)

    def get_messages(self):
        self._clear_messages = True
        return self._messages[:]


def new_messages(sender):
    messages = sender.get_messages()
    for message in messages:
        print('incoming message: {0}'.format(message))


if __name__ == '__main__':
    conn = SocketConnection(('localhost', 5000))
    thread = ConnectionThread(conn)
    thread.new_messages.connect(new_messages)
    thread.run()
