ORDER_LEFT = 0
ORDER_RIGHT = 1
ORDER_DOWN = 2
ORDER_UP = 3


def order_from_char(char):
    if char == "L" or char == "l":
        return ORDER_LEFT
    elif char == "R" or char == "r":
        return ORDER_RIGHT
    elif char == "U" or char == "u":
        return ORDER_DOWN
    elif char == "D" or char == "d":
        return ORDER_UP


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

    def count_correct_puzzles(self):
        correct_puzzles = 0

        for row in range(0, len(self.data)):
            for column in range(1, len(self.data[row])+1):
                if row == len(self.data)-1 and column == len(self.data[row]):
                    true_value = 0
                else:
                    true_value = row * len(self.data[row]) + column
                current_value = self.data[row][column-1]

                if current_value == true_value:
                    correct_puzzles += 1

        return correct_puzzles

    def is_solved(self):
        for row in range(0, len(self.data)):
            for column in range(1, len(self.data[row])+1):
                if row == len(self.data)-1 and column == len(self.data[row]):
                    true_value = 0
                else:
                    true_value = row * len(self.data[row]) + column
                current_value = self.data[row][column-1]

                if true_value != current_value:
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
            if self.blank_column >= 1:
                return True
        elif direction == ORDER_RIGHT:
            if self.blank_column < len(self.data[0])-1:
                return True
        elif direction == ORDER_UP:
            if self.blank_row >= 1:
                return True
        elif direction == ORDER_DOWN:
            if self.blank_row < len(self.data)-1:
                return True
        return False