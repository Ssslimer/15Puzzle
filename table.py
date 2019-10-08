class Table(object):
    def __init__(self, table):
        self.test = 0
        self.data = table

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

                return true_value == current_value

    def print(self):
        print("Table:")
        for row in self.data:
            line = ""
            for value in row:
                line += str(value) + " "
            print(line)
