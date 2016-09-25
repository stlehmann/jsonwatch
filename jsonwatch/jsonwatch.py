"""
Jsonwatch main class

Author: Stefan Lehmann <stefan.st.lehmann@gmail.com>

"""
from . import connection
from .jsonnode import JsonNode


class JsonWatch:

    def __init__(self, connection_: connection.Connection):
        self._connection = connection_

        # create a thread for data exchange
        self._connection_thread = connection.ConnectionThread(self._connection)
        self._connection_thread.new_messages.connect(self._new_messages)
        self._connection_thread.start()
        self.root = JsonNode()

    def _new_messages(self, sender):
        messages = sender.get_messages()
        for message in messages:
            self.root.from_json(message)


if __name__ == '__main__':
    conn = connection.SocketConnection(('localhost', 5000))
    watcher = JsonWatch(conn)
