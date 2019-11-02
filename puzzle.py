import sys
import time

import a_star
import best_first_search
import bfs
import dfs
import idfs
import sma_star
import utils
from table import Table
from utils import order_from_char

BFS = 0
DFS = 1
IDFS = 2
BEST_FIRST_SEARCH = 3
A_STAR = 4
SMA_STAR = 5


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

    time_before = time.time()

    if method == BFS:
        order = build_order(settings[0])
        final_node = bfs.search(begin_table=table, solved_table=solved_table, order=order, max_depth=int(settings[1]), random_orders=order is None)
    elif method == DFS:
        order = build_order(settings[0])
        final_node = dfs.search(begin_table=table, solved_table=solved_table, order=order, max_depth=int(settings[1]), random_orders=order is None)
    elif method == IDFS:
        order = build_order(settings[0])
        final_node = idfs.search(begin_table=table, solved_table=solved_table, order=order, min_limit=int(settings[1]), max_depth=int(settings[2]))
    elif method == BEST_FIRST_SEARCH:
        final_node = best_first_search.search(begin_table=table, solved_table=solved_table, heuristic=int(settings[0]), max_depth=int(settings[1]))
    elif method == A_STAR:
        final_node = a_star.search(begin_table=table, solved_table=solved_table, heuristic=int(settings[0]), max_depth=int(settings[1]))
    elif method == SMA_STAR:
        final_node = sma_star.search()

    if final_node is None:
        print("Could not find a solution!")
        return

    final_node.table.print()
    print("Solution found in " + str(time.time()-time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


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

