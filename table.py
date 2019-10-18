from utils import ORDER_UP, ORDER_DOWN, ORDER_RIGHT, ORDER_LEFT


class Table(object):
    def __init__(self, table):
        self.data = table
        self.blank_row, self.blank_column = self.find_blank_tile_pos()

    def find_blank_tile_pos(self):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                if self.data[row][column] == 0:
                    return row, column

        return -1, -1

    def count_wrong_puzzles(self, proper_table):
        counter = 0

        for row in range(len(self.data)):
            for column in range(1, len(self.data[row])+1):
                if self.data[row][column-1] != proper_table.data[row][column-1]:
                    counter += 1

        return counter

    def is_solved(self, solved_table):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                if self.data[row][column] != solved_table.data[row][column]:
                    return False
        return True

    def print(self):
        print("Table:")
        for row in self.data:
            line = ""
            for value in row:
                line += str(value) + " "
            print(line)

    def move_blank(self, direction):
        if direction == ORDER_LEFT:
            self.__move_blank(0, -1)
        elif direction == ORDER_RIGHT:
            self.__move_blank(0, 1)
        elif direction == ORDER_UP:
            self.__move_blank(-1, 0)
        elif direction == ORDER_DOWN:
            self.__move_blank(1, 0)
        else:
            raise Exception("Wrong direction", direction)

    def __move_blank(self, offset_row, offset_column):
        new_blank_row = self.blank_row + offset_row
        new_blank_column = self.blank_column + offset_column

        self.data[self.blank_row][self.blank_column] = self.data[new_blank_row][new_blank_column]
        self.data[new_blank_row][new_blank_column] = 0
        self.blank_row = new_blank_row
        self.blank_column = new_blank_column

    def can_move(self, direction):
        if direction == ORDER_LEFT:
            return self.blank_column >= 1
        elif direction == ORDER_RIGHT:
            return self.blank_column < len(self.data[0])-1
        elif direction == ORDER_UP:
            return self.blank_row >= 1
        elif direction == ORDER_DOWN:
            return self.blank_row < len(self.data)-1

    def find_value(self, value):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                if self.data[row][column] == value:
                    return row, column

    def __eq__(self, table):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                if self.data[row][column] != table.data[row][column]:
                    return False
        return True
