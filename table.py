from utils import ORDER_UP, ORDER_DOWN, ORDER_RIGHT, ORDER_LEFT


class Table(object):
    def __init__(self, data, blank_row=-1, blank_column=-1):
        self.data = tuple(tuple(item) for item in data)
        self.columns = len(data)
        self.rows = len(data[0])

        if blank_row == -1 or blank_column == -1:
            self.blank_row, self.blank_column = self.find_blank_tile_pos()
        else:
            self.blank_row = blank_row
            self.blank_column = blank_column

        self.hash_value = hash(self.data)

    def find_blank_tile_pos(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.data[row][column] == 0:
                    return row, column

        return -1, -1

    def count_wrong_puzzles(self, proper_table):
        counter = 0

        for row in range(self.rows):
            for column in range(self.columns):
                if self.data[row][column] != proper_table.data[row][column]:
                    counter += 1

        return counter

    def is_solved(self, solved_table):
        return self.hash_value == solved_table.hash_value

    def print(self):
        print("Table:")
        for row in self.data:
            line = ""
            for value in row:
                line += str(value) + " "
            print(line)

    def move_blank(self, direction):
        if direction == ORDER_LEFT:
            return self.__move_blank(0, -1)
        elif direction == ORDER_RIGHT:
            return self.__move_blank(0, 1)
        elif direction == ORDER_UP:
            return self.__move_blank(-1, 0)
        elif direction == ORDER_DOWN:
            return self.__move_blank(1, 0)
        else:
            raise Exception("Wrong direction", direction)

    def can_move(self, direction):
        if direction == ORDER_LEFT:
            return self.blank_column >= 1
        elif direction == ORDER_RIGHT:
            return self.blank_column < self.columns-1
        elif direction == ORDER_UP:
            return self.blank_row >= 1
        elif direction == ORDER_DOWN:
            return self.blank_row < self.rows-1

    def find_value(self, value):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.data[row][column] == value:
                    return row, column

    def __eq__(self, table):
        return table.hash_value == self.hash_value

    def __move_blank(self, offset_row, offset_column):
        new_data = list(list(item) for item in self.data)
        new_blank_row = self.blank_row + offset_row
        new_blank_column = self.blank_column + offset_column

        new_data[self.blank_row][self.blank_column] = new_data[new_blank_row][new_blank_column]
        new_data[new_blank_row][new_blank_column] = 0
        return Table(new_data, new_blank_row, new_blank_column)
