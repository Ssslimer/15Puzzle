import sys

import utils
from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star
from table import Table
from utils import order_from_char


def determine_method(method_argument):
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


def build_standard_solved_table(rows, columns):
    solved_table_data = [[-1 for row in range(rows)] for column in range(columns)]

    for row in range(rows):
        for column in range(1, columns+1):
            solved_table_data[row][column - 1] = row * columns + column

    solved_table_data[-1][-1] = 0

    return Table(solved_table_data)


def build_order(string):
    # Convert from single string to array of numbers corresponding to direction
    if string == "R":
        return None

    if not determine_if_order_correct(string):
        raise Exception("Wrong order, please try again")

    return [order_from_char(string[0]), order_from_char(string[1]), order_from_char(string[2]), order_from_char(string[3])]


def call_algorithm(method, settings, table):
    solved_table = build_standard_solved_table(table.rows, table.columns)

    if method == 0:
        bfs(build_order(settings[0]), solved_table, table)
    elif method == 1:
        dfs(build_order(settings[0]), solved_table, table, max_depth=int(settings[1]))
    elif method == 2:
        idfs(build_order(settings[0]), solved_table, table, min_limit=int(settings[1]), max_depth=int(settings[2]))
    elif method == 3:
        best_first_search(solved_table, table, heuristics=int(settings[0]), max_depth=int(settings[1]))
    elif method == 4:
        a_star(solved_table, table, heuristics=int(settings[0]), max_depth=int(settings[1]))
    elif method == 5:
        sma_star(table, heuristics=int(settings[0]))


def main(args):
    method = determine_method(args[0])

    if method == -1:
        raise Exception("No algorithm was chosen, please try again")

    rows, columns = utils.process_size_input()
    data = utils.process_table_input(rows, columns)
    call_algorithm(method,
                   settings=args[1:],
                   table=Table(data))


if __name__ == '__main__':
    main(sys.argv[1:])

