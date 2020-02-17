from math import floor

import heuristics
from node import Node
import utils


def search(solved_table, begin_table, heuristic, max_depth):
    nodes_to_check = [[Node(begin_table), 0]]
    nodes_to_check_hash = [nodes_to_check[0][0].table.hash_value]
    processed_nodes = list()

    counter = 0
    while len(nodes_to_check) != 0:
        counter += 1

        if counter % 1000 == 0:
            print(str(len(nodes_to_check))+" "+str(counter))

        current_node = nodes_to_check.pop()[0]
        utils.remove_from_descending_list(nodes_to_check_hash, current_node.table.hash_value)
        utils.add_to_ascending_list(processed_nodes, current_node.table.hash_value)

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)
            if child_node.table.is_solved(solved_table):
                return child_node

            value = heuristics.calculate(solved_table, child_node, heuristic)

            if can_node_be_added(child_node, nodes_to_check_hash, processed_nodes, max_depth):
                add_to_descending_list(child_node, value, nodes_to_check)
                utils.add_to_decending_list(nodes_to_check_hash, child_node.table.hash_value)
    return None


def add_to_descending_list(node, value, arr):
    if len(arr) == 0 or value <= arr[-1][1]:
        arr.append([node, value])
        return

    if value >= arr[0][1]:
        arr.insert(0, [node, value])
        return

    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid][1] < value:
            right = mid - 1
        elif arr[mid][1] > value:
            left = mid + 1
        else:
            arr.insert(mid, [node, value])
            return

    if left > right:
        arr.insert(left, [node, value])
        return
    else:
        arr.insert(right, [node, value])
        return


def add_to_descending_list_old(node, value, descending_list):
    for i in range(len(descending_list)):
        if value >= descending_list[i][1]:
            descending_list.insert(i, [node, value])
            return
    descending_list.append([node, value])


def can_node_be_added(node, nodes_to_check_hash, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search_asc(processed_nodes, node.table.hash_value) != -1:
        return False

    if utils.binary_search_asc(nodes_to_check_hash, node.table.hash_value) != -1:
        return False

    return True


def can_node_be_added_old(node, nodes_to_check, processed_nodes, max_depth):
    if node.depth > max_depth:
        return False

    if utils.binary_search_asc(processed_nodes, node.table.hash_value) != -1:
        return False

    for n in nodes_to_check:
        if n[0].table.hash_value == node.table.hash_value:
            return False

    return True
