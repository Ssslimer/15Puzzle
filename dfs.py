from game_tree import Node
import copy
import game_tree
from random import shuffle
import table


def dfs(orders, table):
    # Depth-first search
    print("Inside DFS algorithm")
    tree = game_tree.Tree(table)

    random_orders = orders is None
    final_node = search_in_children(orders, tree, random_orders)
    moves = list()

    current_node = final_node
    while True:
        moves.append(current_node.direction)
        if current_node.parent is None:
            break
        current_node = current_node.parent

    moves.reverse()
    print(convert_moves(moves))


def convert_moves(moves_as_ints):
    moves = list()
    for move in moves_as_ints:
        if move == 0:
            moves.append("L")
        elif move == 1:
            moves.append("R")
        elif move == 2:
            moves.append("D")
        elif move == 3:
            moves.append("U")
    return moves


def search_in_children(orders, tree, random_orders=False):
    nodes_to_check = [tree.root]

    if random_orders:
        orders = [table.ORDER_LEFT, table.ORDER_RIGHT, table.ORDER_DOWN, table.ORDER_UP]
        shuffle(orders)

    while len(nodes_to_check) != 0:
        current_node = nodes_to_check.pop()

        if current_node.table.is_solved():
            print("FOUND SOLUTION")
            current_node.table.print()
            return current_node

        if random_orders:
            shuffle(orders)

        for direction in orders: # TODO add in reversed order
            child_node = Node(copy.deepcopy(current_node.table), current_node, direction)

            if not child_node.table.can_move(direction):
                continue

            child_node.table.move_blank(direction)

            # To prevent from infinite loop we check if the node table is the same as in any of its parents from hierarchy
            if not random_orders and child_node.has_repeated():
                continue

            print(child_node.depth)
            nodes_to_check.append(child_node)
