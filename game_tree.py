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
            if self.is_table_the_same(current_node):
                return True
            if current_node.parent is None:
                return False
            current_node = current_node.parent

    def is_table_the_same(self, node):
        if self.table.blank_column != node.table.blank_column or self.table.blank_row != node.table.blank_row:
            return False

        for row in range(len(self.table.data)):
            for column in range(len(self.table.data[row])):
                if self.table.data[row][column] != node.table.data[row][column]:
                    return False
        return True


class Tree(object):
    def __init__(self, root_table):
        self.root = Node(root_table)

