import sys


def process_size_input():
    print("Pass two integers denoting size of the puzzle table")
    line = input().split()
    if len(line) != 2:
        print("ERROR, expected only 2 integers")

    rows = int(line[0])
    columns = int(line[1])
    if rows <= 1 or columns <= 1:
        print("ERROR, give only positive size for table and at least 2")

    return rows, columns


def process_table_input(rows, columns):
    print("Pass the input")

    input_table = [[0 for x in range(rows)] for y in range(columns)]

    for row in range(0, rows):
        raw_line = input()
        elements = raw_line.split()
        max_value = rows * columns - 1

        if len(elements) != columns:
            print("ERROR, columns and input doesnt match")
        for i in range(0, len(elements)):
            value = int(elements[i])
            if value > max_value:
                print("ERROR, value out of possible range: <0:" + str(max_value)+">")
            input_table[row][i] = value

    return input_table


def main(argv):
    print("Hello there! This is puzzle solver")
    rows, columns = process_size_input()
    table = process_table_input(rows, columns)
    print(table)


main(sys.argv[1:])




