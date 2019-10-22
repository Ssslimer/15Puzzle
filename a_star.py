import utils
from game_tree import Node
import time


def a_star(solved_table, begin_table, heuristics):
    time_before = time.time()

    final_node = search(solved_table, begin_table, heuristics)
    final_node.table.print()
    print("Solution found in " + str(time.time() - time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


def search_hash(solved_table, begin_table, heuristics):
    nodes_to_check = [[Node(begin_table), 0]]  # Node, f(n)
    processed_nodes = dict()  # key=puzzle table hash, value=Node

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        best_entry = nodes_to_check.pop()
        current_node = best_entry[0]

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_table = current_node.table.move_blank(direction)
            child_node = Node(child_table, current_node, direction)

            value = evaluate(solved_table, child_node, heuristics)
            same_table_open_node = find_same_table_node(nodes_to_check, child_node.table)

            if same_table_open_node is not None and child_node.depth > same_table_open_node[0].depth:
                continue

            if child_node.table.hash_value in processed_nodes and child_node.depth > processed_nodes[child_node.table.hash_value].depth:
                continue
            else:
                add_to_descending_list(child_node, value, nodes_to_check)
        processed_nodes[current_node.table.hash_value] = current_node
    raise Exception("Could not find solution")


def search(solved_table, begin_table, heuristics):
    nodes_to_check = [[Node(begin_table), 0]]  # Node, f(n)
    processed_nodes = list()  # Node, f(n)

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        best_entry = nodes_to_check.pop()
        current_node = best_entry[0]

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_table = current_node.table.move_blank(direction)
            child_node = Node(child_table, current_node, direction)

            value = evaluate(solved_table, child_node, heuristics)
            same_table_open_node = find_same_table_node(nodes_to_check, child_node.table)
            same_table_closed_node = find_same_table_node(processed_nodes, child_node.table)

            # Do not choose this way! The node was visited and the route is longer than the previous
            if same_table_closed_node is not None and child_node.depth >= same_table_closed_node[0].depth:
                continue

            if same_table_open_node is not None and child_node.depth >= same_table_open_node[0].depth:
                continue
            else:
                if same_table_open_node is not None:
                    nodes_to_check.remove(same_table_open_node)
                add_to_descending_list(child_node, value, nodes_to_check)
        add_to_descending_list(current_node, best_entry[1], processed_nodes)
    raise Exception("Could not find solution")


def find_same_table_node(nodes, table):
    for n in nodes:
        if n[0].table.hash_value == table.hash_value:
            return n
    return None


def add_to_descending_list(node, value, descending_list):
    for i in range(len(descending_list)):
        if value >= descending_list[i][1]:
            descending_list.insert(i, [node, value])
            return
    descending_list.append([node, value])


def can_node_be_added(node, nodes_to_check, processed_nodes):
    for n in nodes_to_check:
        if n[0].table.hash_value == node.table.hash_value:
            return False

    for n in processed_nodes[node.table.blank_row][node.table.blank_column]:
        if n.table.hash_value == node.table.hash_value:
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
