from node import Node
from random import shuffle
import table
import utils
import time


def dfs(orders, solved_table, begin_table, max_depth):
    time_before = time.time()

    final_node = search(begin_table, solved_table, orders, max_depth=max_depth, random_orders=orders is None)
    final_node.table.print()
    print("Solution found in " + str(time.time()-time_before) + 's')

    moves = utils.create_list_of_moves(final_node)
    print("Moves to solve the puzzle: " + str(len(moves)))
    print(utils.convert_moves(moves))


def search(begin_table, solved_table, orders, max_depth, random_orders=False):
    nodes_to_check = [Node(begin_table)]
    processed_nodes = list()

    if random_orders:
        orders = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(orders)

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1
        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        current_node = nodes_to_check.pop()
        utils.add_to_ascending_list(processed_nodes, current_node.table.hash_value)

        if current_node.table.is_solved(solved_table):
            return current_node

        if random_orders:
            shuffle(orders)

        # Add child nodes to search stack, we want the child with 'first' order on top of the stack, so children
        # should be added in reversed order as top of the "list-stack" is its end
        for i in range(len(orders)-1, -1, -1):
            direction = orders[i]
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)

            if can_node_be_added(child_node, nodes_to_check, processed_nodes, max_depth):
                nodes_to_check.append(child_node)
    raise Exception("SOLUTION NOT FOUND!!")


def can_node_be_added(node, nodes_to_check, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search(processed_nodes, node.table.hash_value) != -1:
        return False

    for n in nodes_to_check:
        if n.table.hash_value == node.table.hash_value:
            return False

    return True
