from typing import List

from game_tree import Node
import copy
from random import shuffle
import table
import utils


def dfs(orders, solved_table, begin_table):
    # Depth-first search
    print("Inside DFS algorithm")

    final_node = search(begin_table, solved_table, orders, random_orders=orders is None)
    print("FOUND SOLUTION")

    moves = utils.create_list_of_moves(final_node)
    print(utils.convert_moves(moves))


def search(begin_table, solved_table, orders, random_orders=False):
    nodes_to_check = [Node(begin_table)]

    # 3D list, we use blank cords to speed up checking
    processed_nodes: List[List[List[Node]]] = [[list() for row in range(len(begin_table.data))] for column in range(len(begin_table.data[0]))]

    if random_orders:
        orders = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(orders)

    count_checked_nodes = 0
    while len(nodes_to_check) != 0:
        if count_checked_nodes % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(count_checked_nodes))
        count_checked_nodes += 1

        current_node = nodes_to_check.pop()
        processed_nodes[current_node.table.blank_row][current_node.table.blank_column].append(current_node)

        if current_node.table.is_solved(solved_table):
            return current_node

        if random_orders:
            shuffle(orders)

        # Add child nodes to search stack, we want the child with 'first' order on top of the stack, so children
        # should be added in reversed order
        for i in range(len(orders)-1, -1, -1):
            direction = orders[i]
            child_node = Node(copy.deepcopy(current_node.table), current_node, direction)

            if not child_node.table.can_move(direction):
                continue

            child_node.table.move_blank(direction)

            if can_node_be_added(child_node, nodes_to_check, processed_nodes):
                nodes_to_check.append(child_node)
    raise Exception("SOLUTION NOT FOUND!!")


def can_node_be_added(node, nodes_to_check, processed_nodes):
    for n in nodes_to_check:
        if n.table == node.table:
            return False

    for n in processed_nodes[node.table.blank_row][node.table.blank_column]:
        if n.table == node.table:
            return False

    return True
