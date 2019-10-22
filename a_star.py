import utils
from game_tree import Node


def a_star(solved_table, begin_table, heuristics):
    print("Inside A* algorithm")

    final_node = search_hash(solved_table, begin_table, heuristics)
    final_node.table.print()
    print("FOUND SOLUTION")

    moves = utils.create_list_of_moves(final_node)
    print(utils.convert_moves(moves))
    print("PATH LENGTH: " + str(len(moves)))


def search_hash(solved_table, begin_table, heuristics):
    nodes_to_check = [[Node(begin_table), 0]]  # Node, f(n)
    if begin_table == solved_table:
        return nodes_to_check[0][0]

    processed_nodes = dict()  # key=puzzle table hash, value=Node

    count_checked_nodes = 0
    while len(nodes_to_check) != 0:
        best_entry = nodes_to_check.pop()
        current_node = best_entry[0]

        count_checked_nodes += 1

        if count_checked_nodes % 100 == 0:
            print("CHECKED: " + str(count_checked_nodes))
            print(str(best_entry[1])+" "+str(best_entry[0].depth))

        if current_node.table.is_solved(solved_table):
            print("FOUND")
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
    if begin_table == solved_table:
        return nodes_to_check[0][0]

    processed_nodes = list()  # Node, f(n)

    count_checked_nodes = 0
    while len(nodes_to_check) != 0:
        best_entry = nodes_to_check.pop()
        current_node = best_entry[0]

        count_checked_nodes += 1

        if count_checked_nodes % 100 == 0:
            print("CHECKED: " + str(count_checked_nodes))
            print(str(best_entry[1])+" "+str(best_entry[0].depth))
        if count_checked_nodes == 50000:
            return current_node

        if current_node.table.is_solved(solved_table):
            print("FOUND")
            return current_node

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_table = current_node.table.move_blank(direction)
            child_node = Node(child_table, current_node, direction)

            value = evaluate(solved_table, child_node, heuristics)
            same_table_open_node = find_same_table_node(nodes_to_check, child_node.table)
            same_table_closed_node = find_same_table_node(processed_nodes, child_node.table)

            if same_table_open_node is not None and child_node.depth > same_table_open_node[0].depth:
                continue

            if same_table_closed_node is not None and child_node.depth > same_table_closed_node[0].depth:
                continue
            else:
                add_to_descending_list(child_node, value, nodes_to_check)
        add_to_descending_list(current_node, best_entry[1], processed_nodes)
    raise Exception("Could not find solution")


def find_same_table_node(nodes, table):
    for n in nodes:
        if n[0].table == table:
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
        if n[0].table == node.table:
            return False

    for n in processed_nodes[node.table.blank_row][node.table.blank_column]:
        if n.table == node.table:
            return False

    return True


def evaluate(solved_table, node, heuristics):
    if heuristics == 0:
        value = node.table.count_wrong_puzzles(solved_table)
        return value + node.depth
    elif heuristics == 1:
        manhattan_distance_sum = 0

        for row in range(len(solved_table.data)):
            for column in range(len(solved_table.data[row])):
                value = solved_table.data[row][column]
                actual_row, actual_column = node.table.find_value(value)
                manhattan_distance_sum += abs(actual_row - row) + abs(actual_column - column)

        return manhattan_distance_sum + node.depth
    elif heuristics == 2:
        error_sum = 0

        for row in range(len(solved_table.data)):
            for column in range(len(solved_table.data[row])):
                proper_value = solved_table.data[row][column]
                value = node.table.data[row][column]
                error_sum += abs(proper_value - value)

        return error_sum + node.depth
