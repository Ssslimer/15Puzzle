import sys

from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star
from table import Table
from utils import order_from_char


def determine_method():
    method_argument = sys.argv[1]
    if method_argument == "-b" or method_argument == "-bfs":
        return 0
    elif method_argument == "-d" or method_argument == "-dfs":
        return 1
    elif method_argument == "-i" or method_argument == "-idfs":
        return 2
    elif method_argument == "-h" or method_argument == "-bf":
        return 3
    elif method_argument == "-a" or method_argument == "-astar":
        return 4
    elif method_argument == "-s" or method_argument == "-sma":
        return 5
    raise Exception("No such method implemented")


def determine_if_order_correct(order):
    if len(order) != 4:
        return False

    return "L" in order and "R" in order and "U" in order and "D" in order


def call_algorithm(method, order, table):
    solved_table = [[-1 for row in range(len(table.data))] for column in range(len(table.data[0]))]
    for row in range(len(table.data)):
        for column in range(1, len(table.data[row])+1):
            solved_table[row][column - 1] = row * len(table.data[row]) + column
    solved_table[-1][-1] = 0

    if method == 0:
        bfs(order, Table(solved_table), table)
    elif method == 1:
        dfs(order, Table(solved_table), table)
    elif method == 2:
        idfs(order, table)
    elif method == 3:
        best_first_search(Table(solved_table), table, heuristics=0)
    elif method == 4:
        a_star(Table(solved_table), table, heuristics=0)
    elif method == 5:
        sma_star(order, table)


def process_size_input():
    print("Pass two integers denoting size of the puzzle table")
    line = input().split()
    if len(line) != 2:
        raise Exception("ERROR, expected only 2 integers")

    rows = int(line[0])
    columns = int(line[1])
    if rows <= 1 or columns <= 1:
        raise Exception("ERROR, give only positive size for table and at least 2")

    return rows, columns


def process_table_input(rows, columns):
    print("Pass the input")

    input_table = [[0 for x in range(rows)] for y in range(columns)]

    for row in range(rows):
        raw_line = input()
        elements = raw_line.split()
        max_value = rows * columns - 1

        if len(elements) != columns:
            raise Exception("ERROR, columns and input doesnt match")
        for i in range(len(elements)):
            value = int(elements[i])
            if value > max_value:
                raise Exception("ERROR, value out of possible range: <0:" + str(max_value)+">")
            input_table[row][i] = value

    # Used to check if the numbers are fine
    validation_list = [False] * (rows * columns)

    for row in range(rows):
        for column in range(columns):
            validation_list[input_table[row][column]] = True

    for b in validation_list:
        if not b:
            raise Exception("ERROR, INCORRECT NUMBERS", validation_list)

    return input_table


def main(argv):
    method = determine_method()
    order = sys.argv[2]

    if method == -1:
        raise Exception("No algorithm was chosen, please try again")

    if order == "R":
        order = None
    else:
        if not determine_if_order_correct(order):
            raise Exception("Wrong order, please try again")
        else:
            order = [order_from_char(order[0]), order_from_char(order[1]), order_from_char(order[2]), order_from_char(order[3])]

    print("Hello there! This is puzzle solver")
    rows, columns = process_size_input()
    table = Table(process_table_input(rows, columns))

    # Convert from single string to array of numbers corresponding to direction

    call_algorithm(method, order, table)


main(sys.argv[1:])
