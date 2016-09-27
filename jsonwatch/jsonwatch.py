"""
Jsonwatch main class

Author: Stefan Lehmann <stefan.st.lehmann@gmail.com>

"""
from . import connection
from .jsonnode import JsonNode


class JsonWatch:

    def __init__(self, connection_: connection.Connection):
        self._connection = connection_
        self.root = JsonNode()

        # create a thread for data exchange
        self._connection_thread = connection.ConnectionThread(self._connection)
        self._connection_thread.new_messages.connect(self._new_messages)
        self._connection_thread.start()

    def _new_messages(self, sender):
        messages = sender.get_messages()
        for message in messages:
            self.root.from_json(message)

    def disconnect(self):
        self._connection_thread.stop()

    def tree(self):
        def _print_tree(level, _node):
            for child in _node:
                print('  ' * level + '|- ' + child.key + ': ' + str(child.value))
                if isinstance(child, JsonNode):
                    _print_tree(level + 1, child)

        print('\nroot')
        _print_tree(1, self.root)
        print('\n')


if __name__ == '__main__':
    import time

    conn = connection.SocketConnection(('localhost', 5000))
    watcher = JsonWatch(conn)
    time.sleep(2)
    watcher.tree()
