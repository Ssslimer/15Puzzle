import utils
from node import Node
import time


def a_star(solved_table, begin_table, heuristics, max_depth=140):
    time_before = time.time()

    heuristics = 1
    final_node = search(solved_table, begin_table, heuristics, max_depth)
    final_node.table.print()
    print("Solution found in " + str(time.time() - time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


def search(solved_table, begin_table, heuristics, max_depth):
    open_nodes = [[Node(begin_table), 0]]  # Node, f(n)
    closed_nodes = list()  # Node, f(n)

    counter = 0
    while len(open_nodes) != 0:
        counter += 1
        if counter % 1000 == 0:
            print("Open nodes: "+str(len(open_nodes))+" Closed nodes: "+str(len(closed_nodes))+" "+str(counter)+" "+str(open_nodes[-1][0].depth))

        current_node, current_f = open_nodes.pop()

        if current_node.table.is_solved(solved_table):
            return current_node

        if current_node.depth > max_depth:
            continue

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)

            h = calculate_h(solved_table, child_node, heuristics)
            g = calculate_g(child_node)
            f = h + g

            same_table_open_node = find_same_table_node(open_nodes, child_node.table)
            same_table_closed_node = find_same_table_node(closed_nodes, child_node.table)

            if same_table_open_node is None and same_table_closed_node is None:
                # The node is reached for the 1st time, so we can easily add it
                add_to_descending_list(child_node, f, open_nodes)
            elif same_table_open_node is not None and g < same_table_open_node[0].depth:
                # We found better route to the Node
                remove_from_descending_list(same_table_open_node[1], open_nodes)
                add_to_descending_list(child_node, f, open_nodes)
            elif same_table_closed_node is not None:# and g < same_table_closed_node[0].depth:
                continue
                #add_to_descending_list(child_node, f, open_nodes)

        add_to_descending_list(current_node, current_f, closed_nodes)
    raise Exception("Could not find solution")


def search_dict(solved_table, begin_table, heuristics, max_depth):
    open_nodes = [[Node(begin_table), 0]]  # Node, f(n)
    closed_nodes = dict()  # value=Node, key=hash

    counter = 0
    while len(open_nodes) != 0:
        counter += 1
        if counter % 1000 == 0:
            print("Open nodes: "+str(len(open_nodes))+" Closed nodes: "+str(len(closed_nodes))+" "+str(counter)+" "+str(open_nodes[-1][0].depth))

        current_node, current_f = open_nodes.pop()

        if current_node.table.is_solved(solved_table):
            return current_node

        if current_node.depth > max_depth:
            continue

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)

            h = calculate_h(solved_table, child_node, heuristics)
            g = calculate_g(child_node)
            f = h + g

            same_table_open_node = find_same_table_node(open_nodes, child_node.table)
            same_table_closed_node = child_node.table.hash_value in closed_nodes

            if same_table_open_node is None and same_table_closed_node is None:
                # The node is reached for the 1st time, so we can easily add it
                add_to_descending_list(child_node, f, open_nodes)
            elif same_table_open_node is not None and g < same_table_open_node[0].depth:
                # We found better route to the Node
                remove_from_descending_list(same_table_open_node[1], open_nodes)
                add_to_descending_list(child_node, f, open_nodes)
            elif same_table_closed_node is not None:
                continue

        #add_to_descending_list(current_node, current_f, closed_nodes)
        closed_nodes[current_node.table.hash_value] = current_node
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
