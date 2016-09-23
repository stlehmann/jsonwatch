#!-*- coding: utf-8 -*-
"""
Module for diffent connections.

:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com

"""
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

    def connect(self):
        self.serial.open()

    def disconnect(self):
        self.serial.close()

    def send(self, data):
        return self.serial.write(data)

    def receive(self, size=1):
        return self.serial.read(size)

    @property
    def connected(self):
        return self.serial.is_open()


class SocketConnection(Connection):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = False

    def connect(self, host=None, port=None):
        self.socket.connect((host, port))
        self._connected = True

    def disconnect(self):
        self.socket.close()
        self._connected = False

    def send(self, data: bytes):
        return self.socket.send(bytes)

    def receive(self):
        return self.socket.recvfrom(4096)

    @property
    def connected(self):
        return self._connected


class ConnectionThread(threading.Thread):
    def __init__(self, connection, *args, **kwargs):
        self.connection = connection
        self._run = True

        super(ConnectionThread, self).__init__(*args, **kwargs)

    def run(self):
        while self._run:
            data = self.connection.receive()
            logger.info('incoming message: {0}'.format(data))
