from game_tree import Node
import copy
from random import shuffle
import table
import utils


def bfs(order, solved_table, begin_table):
    # Breadth-first search
    print("Inside BFS algorithm")

    final_node = search(begin_table, solved_table, order, random_orders=order is None)
    print("FOUND SOLUTION")

    moves = utils.create_list_of_moves(final_node)
    print(utils.convert_moves(moves))


def search(begin_table, solved_table, order, random_orders=False):
    nodes_to_check = [Node(begin_table)]

    # List of hashes
    processed_nodes = list()

    if random_orders:
        orders = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(orders)

    count_checked_nodes = 0

    while True:
        # if count_checked_nodes % 20 == 0:
        print(str(len(nodes_to_check)) + " " + str(count_checked_nodes))
        count_checked_nodes += len(nodes_to_check)

        new_nodes_to_check = []
        for node in nodes_to_check:
            utils.add_to_ascending_list(processed_nodes, node.table.hash_value)
            if node.table.is_solved(solved_table):
                return node
            else:
                for i in range(len(order)):
                    direction = order[i]
                    # child_node = Node(copy.deepcopy(node.table), node, direction)

                    if not node.table.can_move(direction):
                        continue

                    child_table = node.table.move_blank(direction)
                    child_node = Node(child_table, node, direction)

                    if can_node_be_added(child_node, new_nodes_to_check, processed_nodes):
                        new_nodes_to_check.append(child_node)

        nodes_to_check = new_nodes_to_check

    raise Exception("SOLUTION NOT FOUND!!")


def can_node_be_added(node, nodes_to_check, processed_nodes):
    max_depth = 1000

    if node.depth > max_depth:
        return False

    for n in nodes_to_check:
        if n.table.hash_value == node.table.hash_value:
            return False

    if utils.binary_search(processed_nodes, node.table.hash_value) != -1:
        return False

    return True
