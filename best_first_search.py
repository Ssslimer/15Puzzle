from math import floor

from node import Node
import utils
import time


def best_first_search(solved_table, begin_table, heuristics, max_depth):
    time_before = time.time()

    final_node = search(solved_table, begin_table, heuristics=heuristics, max_depth=max_depth)
    final_node.table.print()
    print("Solution found in " + str(time.time()-time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


def search(solved_table, begin_table, heuristics, max_depth):
    nodes_to_check = [[Node(begin_table), 0]]
    nodes_to_check_hash = [nodes_to_check[0][0].table.hash_value]
    processed_nodes = list()

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1

        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        current_node = nodes_to_check.pop()[0]
        utils.remove_from_descending_list(nodes_to_check_hash, current_node.table.hash_value)
        utils.add_to_ascending_list(processed_nodes, current_node.table.hash_value)

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)
            value = evaluate(solved_table, child_node, heuristics)

            if can_node_be_added(child_node, nodes_to_check_hash, processed_nodes, max_depth):
                add_to_descending_list(child_node, value, nodes_to_check)
                utils.add_to_decending_list(nodes_to_check_hash, child_node.table.hash_value)
    raise Exception("Could not find solution")


def search_old(solved_table, begin_table, heuristics, max_depth):
    nodes_to_check = [[Node(begin_table), 0]]
    processed_nodes = list()

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        current_node = nodes_to_check.pop()[0]
        utils.add_to_ascending_list(processed_nodes, current_node.table.hash_value)

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)
            value = evaluate(solved_table, child_node, heuristics)

            if can_node_be_added_old(child_node, nodes_to_check, processed_nodes, max_depth):
                add_to_descending_list_old(child_node, value, nodes_to_check)
    raise Exception("Could not find solution")


def add_to_descending_list(node, value, arr):
    if len(arr) == 0 or value <= arr[-1][1]:
        arr.append([node, value])
        return

    if value >= arr[0][1]:
        arr.insert(0, [node, value])
        return

    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid][1] < value:
            right = mid - 1
        elif arr[mid][1] > value:
            left = mid + 1
        else:
            arr.insert(mid, [node, value])
            return

    if left > right:
        arr.insert(left, [node, value])
        return
    else:
        arr.insert(right, [node, value])
        return


def add_to_descending_list_old(node, value, descending_list):
    for i in range(len(descending_list)):
        if value >= descending_list[i][1]:
            descending_list.insert(i, [node, value])
            return
    descending_list.append([node, value])


def can_node_be_added(node, nodes_to_check_hash, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search(processed_nodes, node.table.hash_value) != -1:
        return False

    if utils.binary_search(nodes_to_check_hash, node.table.hash_value) != -1:
        return False

    return True


def can_node_be_added_old(node, nodes_to_check, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search(processed_nodes, node.table.hash_value) != -1:
        return False

    for n in nodes_to_check:
        if n[0].table.hash_value == node.table.hash_value:
            return False

    return True


def evaluate(solved_table, node, heuristics):
    if heuristics == 0:
        value = node.table.count_wrong_puzzles(solved_table)
        return value
    elif heuristics == 1:
        manhattan_distance_sum = 0

        for row in range(node.table.rows):
            for column in range(node.table.columns):
                value = solved_table.data[row][column]
                actual_row, actual_column = node.table.find_value(value)
                manhattan_distance_sum += abs(actual_row - row) + abs(actual_column - column)

        return manhattan_distance_sum
    elif heuristics == 2:
        weighted_sum = 0
        for row in range(node.table.rows):
            for column in range(node.table.columns):
                if node.table.data[row][column] != solved_table.data[row][column]:
                    if column < row:
                        weighted_sum += node.table.columns - column
                    else:
                        weighted_sum += node.table.rows - row

        return weighted_sum
