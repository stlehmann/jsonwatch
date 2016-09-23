#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com

"""
import json
import atexit
import logging
import threading
import socket
import select


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: %(message)s')
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

null_logger = logging.getLogger(__name__ + '_null')
null_logger.addHandler(logging.NullHandler)

PORT = 5000


class TestServer(threading.Thread):
    """
    :summary: Simple Testserver

    """

    def __init__(self, handler=None, ip_address='', port=PORT, logging=True,
                 *args, **kwargs):
        self.handler = handler or default_handler
        self.ip_address = ip_address
        self.port = port
        self._run = True

        global logger
        logger = logger if logging else null_logger

        # keep track of all received packets
        self.request_history = []
        # conainer for client connection threads
        self.clients = []

        # initialize socket server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # option to allow instant socket reuse after termination
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip_address, self.port))

        # cleanup on exit
        atexit.register(self.close)

        super(TestServer, self).__init__(*args, **kwargs)
        self.daemon = True

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def stop(self):
        """
        :summary: Close client connections and stop main server loop.

        """
        for client in self.clients:
            client.close()

        self.clients = []

        if self._run:
            logger.info('Stopping server thread.')
            self._run = False
        self.server.close()

    def close(self):
        self.stop()

    def run(self):
        """
        :summary: Listen for incoming connections from clients.

        """
        self._run = True

        # start listening
        self.server.listen(5)

        logger.info('Server listening on {0}:{1}'.format(
            self.ip_address or 'localhost', self.port
        ))

        # server loop
        while self._run:
            # check for new connections at server socket
            ready, _, _ = select.select([self.server], [], [], 0.1)

            if ready:
                # accept connections from clients
                try:
                    client, address = self.server.accept()
                except:
                    continue

                logger.info('New connection from {0}:{1}'.format(*address))

                # delegate handling of connection to client thread
                client_thread = ClientConnection(
                    handler=self.handler, client=client, address=address,
                    server=self
                )
                client_thread.daemon = True
                client_thread.start()
                self.clients.append(client_thread)


class ClientConnection(threading.Thread):
    def __init__(self, handler, client, address, server, *args, **kwargs):
        self.handler = handler
        self.server = server
        self.client = client
        self.client_address = address

        # cleanup on exit
        atexit.register(self.close)

        # server loop execution flag
        self._run = True

        # timer for status messages
        self.stop_flag = threading.Event()
        self._timer = TimerThread(self.client, self.client_address,
                                  self.stop_flag)
        self._timer.start()

        super(ClientConnection, self).__init__(*args, **kwargs)

    def stop(self):
        if self._run:
            logger.info(
                'Closing client connection {0}:{1}.'
                .format(*self.client_address)
            )
            self._run = False
        self.join()

    def close(self):
        if self.is_alive():
            self.stop()
        self.client.close()

    def run(self):
        """
        :summary: Listen for data on client connection

        """
        self._run = True

        # main listening loop
        while self._run:
            ready, _, _ = select.select([self.client], [], [], 0.1)

            if not ready:
                continue

            data, _ = self.client.recvfrom(4096)

            if not data:
                self.client.close()
                self._run = False
                continue

            # add request to request history
            self.server.request_history.append(data)

            # delegate request and get response data
            response = self.handler(data)

            # send response to client
            self.client.send(response)

    def send_message(self):
        self.client.send(b'hello world')


class TimerThread(threading.Thread):
    def __init__(self, client, client_address, event):
        super(TimerThread, self).__init__()
        self.stopped = event
        self.client = client
        self.client_address = client_address

    def run(self):
        while not self.stopped.wait(1.0):
            try:
                data = json.dumps({
                    'a': 1,
                    'b': 2
                })
                self.client.send(data.encode())
                logger.info('Sent {data} to {adr[0]}:{adr[1]}'.format(
                    data=data, adr=self.client_address))
            except OSError:
                logger.info('Connection to {0}:{1} closed'.format(
                    self.client_address[0], self.client_address[1]))
                return


def default_handler(request):
    logger.info(request)
    return request


if __name__ == '__main__':
    server = TestServer()
    try:
        server.start()
        server.join()
    except:
        server.close()
