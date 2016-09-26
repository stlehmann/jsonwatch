#!-*- coding: utf-8 -*-
"""
Module for diffent connections.

:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com

"""
from serial import Serial
import socket


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

    def read(self, size=1):
        return self.serial.read(size)

    def write(self, data):
        return self.serial.write(data)


class SocketConnection(Connection):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host=None, port=None):
        self.socket.connect((host, port))
