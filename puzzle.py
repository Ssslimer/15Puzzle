import sys
from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star


def main(argv):
    if sys.argv[1] == "-b" or sys.argv[1] == "-bfs":
        print("BFS")
        bfs()
    elif sys.argv[1] == "-d" or sys.argv[1] == "-dfs":
        print("DFS")
        dfs()
    elif sys.argv[1] == "-i" or sys.argv[1] == "-idfs":
        print("IDFS")
        idfs()
    elif sys.argv[1] == "-h" or sys.argv[1] == "-bf":
        print("Best first search")
        best_first_search()
    elif sys.argv[1] == "-a" or sys.argv[1] == "-astar":
        print("A*")
        a_star()
    elif sys.argv[1] == "-s" or sys.argv[1] == "-sma":
        print("SMA*")
        sma_star()
    else:
        print("No algorithm was chosen, please try again")


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

    # Used to check if the numbers are fine
    validation_list = [False] * (rows * columns)

    for row in range(0, rows):
        for column in range(0, columns):
            validation_list[input_table[row][column]] = True

    for b in validation_list:
        if not b:
            print("ERROR, INCORRECT NUMBERS")

    return input_table


def print_table(table):
    print("Table:")
    for row in table:
        line = "";
        for value in row:
            line += str(value) +" "
        print(line)


def main(argv):
    print("Hello there! This is puzzle solver")
    rows, columns = process_size_input()
    table = process_table_input(rows, columns)
    print_table(table)


main(sys.argv[1:])




