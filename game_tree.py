class Node(object):
    def __init__(self, table, parent=None, direction=-1):
        self.table = table
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

        # How the node table was obtained from the previous table
        self.direction = direction

    def has_repeated(self):
        current_node = self.parent

        while True:
            if self == current_node:
                return True
            if current_node.parent is None:
                return False
            current_node = current_node.parent
