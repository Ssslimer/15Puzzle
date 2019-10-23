import utils
from node import Node
import time


def a_star(solved_table, begin_table, heuristics):
    time_before = time.time()

    heuristics = 2
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

            h = calculate_h(solved_table, child_node, heuristics)
            f = h + child_node.depth
            same_table_open_node = find_same_table_node(nodes_to_check, child_node.table)

            if same_table_open_node is not None and child_node.depth > same_table_open_node[0].depth:
                continue

            if child_node.table.hash_value in processed_nodes and child_node.depth > processed_nodes[child_node.table.hash_value].depth:
                continue
            else:
                add_to_descending_list(child_node, f, nodes_to_check)
        processed_nodes[current_node.table.hash_value] = current_node
    raise Exception("Could not find solution")


def search(solved_table, begin_table, heuristics):
    nodes_to_check = [[Node(begin_table), 0]]  # Node, f(n)
    processed_nodes = list()  # Node, f(n)

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
       # if counter % 1 == 0:
            #print(str(len(nodes_to_check))+" "+str(counter)+" "+str(nodes_to_check[-1][1]))

        current_node, current_f = nodes_to_check.pop()
        current_node.table.print()

        if current_node.table.is_solved(solved_table):
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)

            h = calculate_h(solved_table, child_node, heuristics)
            g = calculate_g(child_node)
            f = h + g

            same_table_open_node = find_same_table_node(nodes_to_check, child_node.table)
            same_table_closed_node = find_same_table_node(processed_nodes, child_node.table)

            # Node has been visited but the new road is worse so skip this road
            if same_table_closed_node is not None and g >= same_table_closed_node[0].depth:
                continue

            # Its is better to move to the Node with the new route
            if same_table_open_node is not None:
                if g < same_table_open_node[0].depth:
                    print("TEST")
                    print(nodes_to_check)
                    remove_from_descending_list(same_table_open_node[1], nodes_to_check)
                    print(nodes_to_check)
                    add_to_descending_list(child_node, f, nodes_to_check)
            else:
                add_to_descending_list(child_node, f, nodes_to_check)
        add_to_descending_list(current_node, current_f, processed_nodes)
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


def remove_from_descending_list(value, descending_list):
    for i in range(len(descending_list)):
        if value == descending_list[i][1]:
            del descending_list[i]
            return


def can_node_be_added(node, nodes_to_check, processed_nodes):
    for n in nodes_to_check:
        if n[0].table.hash_value == node.table.hash_value:
            return False

    for n in processed_nodes[node.table.blank_row][node.table.blank_column]:
        if n.table.hash_value == node.table.hash_value:
            return False

    return True


def calculate_g(node):
    return node.depth


def calculate_h(solved_table, node, heuristics):
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
