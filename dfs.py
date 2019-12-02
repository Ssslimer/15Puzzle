from node import Node
from random import shuffle
import table
import utils


def search(begin_table, solved_table, order, max_depth, random_orders=False):
    nodes_to_check = [Node(begin_table)]
    processed_nodes = list()

    if random_orders:
        order = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(order)

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        current_node = nodes_to_check.pop()
        utils.add_to_ascending_list(processed_nodes, current_node.table.hash_value)

        if random_orders:
            shuffle(order)

        # Add child nodes to search stack, we want the child with 'first' order on top of the stack, so children
        # should be added in reversed order as top of the "list-stack" is its end
        for direction in reversed(order):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)
            if child_node.table.is_solved(solved_table):
                return child_node

            if can_node_be_added(child_node, nodes_to_check, processed_nodes, max_depth):
                nodes_to_check.append(child_node)
    return None


def can_node_be_added(node, nodes_to_check, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search_asc(processed_nodes, node.table.hash_value) != -1:
        return False

    for n in nodes_to_check:
        if n.table.hash_value == node.table.hash_value:
            return False

    return True
