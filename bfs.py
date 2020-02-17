from node import Node
from random import shuffle
import table
import utils


def search(begin_table, solved_table, max_depth, order=None, random_orders=False):
    nodes_to_check = [Node(begin_table)]
    processed_nodes = list()

    if random_orders:
        order = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(order)

    count_checked_nodes = 0
    for depth in range(max_depth):
        print("Depth:" + str(depth) + " " + str(len(nodes_to_check)) + " " + str(count_checked_nodes))
        count_checked_nodes += len(nodes_to_check)

        new_nodes_to_check = []
        for node in nodes_to_check:
            utils.add_to_ascending_list(processed_nodes, node.table.hash_value)

            for i in range(len(order)):
                direction = order[i]

                if not node.table.can_move(direction):
                    continue

                child_node = Node(node.table.move_blank(direction), node, direction)
                if child_node.table.is_solved(solved_table):
                    return child_node

                if can_node_be_added(child_node, new_nodes_to_check, processed_nodes):
                    new_nodes_to_check.append(child_node)
        nodes_to_check = new_nodes_to_check
    return None


def can_node_be_added(node, nodes_to_check, processed_nodes):
    if utils.binary_search_asc(processed_nodes, node.table.hash_value) != -1:
        return False

    for n in nodes_to_check:
        if n.table.hash_value == node.table.hash_value:
            return False

    return True
