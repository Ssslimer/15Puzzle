class Table(object):
    def __init__(self, table):
        self.test = 0
        self.data = table

    def is_solved(self):
        for i in range(0, len(self.table)):
            for j in range(0, len(self.table[i])):
                print(self.table[i][j])
