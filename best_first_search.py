from typing import List

from game_tree import Node
import copy
import utils


def best_first_search(solved_table, begin_table, heuristics):
    # Best-first search
    print("Inside Best-first search algorithm")

    final_node = search(solved_table, begin_table, heuristics)
    print("FOUND SOLUTION")

    moves = utils.create_list_of_moves(final_node)
    print(utils.convert_moves(moves))
    print("PATH LENGTH: " + str(len(moves)))


def search(solved_table, begin_table, heuristics):
    nodes_to_check = [[Node(begin_table), 0]]

    # 3D list, we use blank cords to speed up checking
    processed_nodes: List[List[List[Node]]] = [[list() for row in range(len(solved_table.data))] for column in range(len(solved_table.data[0]))]

    count_checked_nodes = 0
    while len(nodes_to_check) != 0:
        current_node = nodes_to_check.pop()[0]
        processed_nodes[current_node.table.blank_row][current_node.table.blank_column].append(current_node)

        count_checked_nodes += 1

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            child_node = Node(copy.deepcopy(current_node.table), current_node, direction)

            if not child_node.table.can_move(direction):
                continue

            child_node.table.move_blank(direction)
            value = evaluate(solved_table, child_node, heuristics)
            if count_checked_nodes % 100 == 0:
                print(str(child_node.depth) + " " + str(len(nodes_to_check)) + " " + str(value) + " checked_nodes=" + str(count_checked_nodes))

            if can_node_be_added(child_node, nodes_to_check, processed_nodes):
                add_to_descending_list(child_node, value, nodes_to_check)

    raise Exception("Could not find solution")


def add_to_descending_list(node, value, descending_list):
    for i in range(len(descending_list)-1, -1, -1):
        if value < descending_list[i][1]:
            descending_list.insert(i+1, [node, value])
            return
    descending_list.append([node, value])


def can_node_be_added(node, nodes_to_check, processed_nodes):
    for n in nodes_to_check:
        if n[0].table == node.table:
            return False

    for n in processed_nodes[node.table.blank_row][node.table.blank_column]:
        if n.table == node.table:
            return False

    return True


def evaluate(proper_table, node, heuristics):
    if heuristics == 0:
        value = node.table.count_wrong_puzzles(proper_table)
        return value
    elif heuristics == 1:
        manhattan_distance_sum = 0

        for row in range(len(proper_table)):
            for column in range(len(proper_table[row])):
                value = proper_table[row][column]
                actual_row, actual_column = node.table.find_value(value)
                manhattan_distance_sum += abs(actual_row - row) + abs(actual_column - column)

        return manhattan_distance_sum
    elif heuristics == 2:
        error_sum = 0

        for row in range(len(proper_table)):
            for column in range(len(proper_table[row])):
                proper_value = proper_table[row][column]
                value = node.table.data[row][column]
                error_sum += abs(proper_value - value)

        return error_sum
