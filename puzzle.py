import sys
import random
from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star


def determine_method():
    if sys.argv[1] == "-b" or sys.argv[1] == "-bfs":
        return 0
    elif sys.argv[1] == "-d" or sys.argv[1] == "-dfs":
        return 1
    elif sys.argv[1] == "-i" or sys.argv[1] == "-idfs":
        return 2
    elif sys.argv[1] == "-h" or sys.argv[1] == "-bf":
        return 3
    elif sys.argv[1] == "-a" or sys.argv[1] == "-astar":
        return 4
    elif sys.argv[1] == "-s" or sys.argv[1] == "-sma":
        return 5
    else:
        return -1


def create_random_order():
    order_options = ["L", "R", "D", "U"]
    order = ""

    for i in range(4):
        while True:
            option_index = random.randint(0, 3)
            if order_options[option_index] not in order:
                order += order_options[option_index]
                break

    return order


def determine_if_order_correct(order):
    if len(order) == 4:
        if "L" in order and "R" in order and "U" in order and "D" in order:
            return True
        else:
            return False
    else:
        return False


def call_algorithm(method, order):
    if method == 0:
        bfs(order)
    elif method == 1:
        dfs(order)
    elif method == 2:
        idfs(order)
    elif method == 3:
        best_first_search(order)
    elif method == 4:
        a_star(order)
    elif method ==  5:
        sma_star(order)


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
    method = determine_method()
    order = sys.argv[2]
    # is_order_correct

    if order == "R":
        order = create_random_order()
        is_order_correct = True
        print("Random order: " + order)
    else:
        is_order_correct = determine_if_order_correct(order)

    if method == -1:
        print("No algorithm was chosen, please try again")
        return

    if not is_order_correct:
        print("Wrong order, please try again")
        return

    print(order + " order chosen")
    print("Hello there! This is puzzle solver")
    rows, columns = process_size_input()
    table = process_table_input(rows, columns)
    print_table(table)

    call_algorithm(method, order)


main(sys.argv[1:])