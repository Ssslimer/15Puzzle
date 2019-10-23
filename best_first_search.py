from node import Node
import utils
import time


def best_first_search(solved_table, begin_table, heuristics):
    time_before = time.time()

    final_node = search(solved_table, begin_table, heuristics)
    final_node.table.print()
    print("Solution found in " + str(time.time()-time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


def search(solved_table, begin_table, heuristics):
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

            if can_node_be_added(child_node, nodes_to_check, processed_nodes):
                add_to_descending_list(child_node, value, nodes_to_check)
    raise Exception("Could not find solution")


def add_to_descending_list(node, value, descending_list):
    for i in range(len(descending_list)):
        if value >= descending_list[i][1]:
            descending_list.insert(i, [node, value])
            return
    descending_list.append([node, value])


def can_node_be_added(node, nodes_to_check, processed_nodes):
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

        for row in range(len(solved_table.data)):
            for column in range(len(solved_table.data[row])):
                value = solved_table.data[row][column]
                actual_row, actual_column = node.table.find_value(value)
                manhattan_distance_sum += abs(actual_row - row) + abs(actual_column - column)

        return manhattan_distance_sum
    elif heuristics == 2:
        cartesian_distance_sum = 0

        for row in range(len(solved_table.data)):
            for column in range(len(solved_table.data[row])):
                value = solved_table.data[row][column]
                actual_row, actual_column = node.table.find_value(value)
                delta_row = actual_row - row
                delta_column = actual_column - column
                cartesian_distance_sum += pow(delta_row*delta_row + delta_column*delta_column, 0.5)

        return cartesian_distance_sum
