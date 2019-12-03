from math import floor

import heuristics
import utils
from node import Node


def search(solved_table, begin_table, heuristic, max_depth):
    open_nodes = [[Node(begin_table), 0]]  # Node, f(n)
    open_nodes_hash = [[open_nodes[0][0], open_nodes[0][0].table.hash_value]]  # [Node, Node.table.hashcode]
    closed_nodes = list()  # hashcodes

    counter = 0
    while len(open_nodes) != 0:
        counter += 1
        if counter % 1000 == 0:
            print("Open nodes: "+str(len(open_nodes))+" Closed nodes: "+str(len(closed_nodes))+" "+str(counter)+" "+str(open_nodes[-1][0].depth))

        current_node, current_f = open_nodes.pop()
        remove_from_ascending_list(open_nodes_hash, current_node.table.hash_value)  # Remove corresponding hash+node entry

        if current_node.table.is_solved(solved_table):
            return current_node

        if current_node.depth > max_depth:
            continue

        for direction in range(4):
            if not current_node.table.can_move(direction):
                continue

            child_node = Node(current_node.table.move_blank(direction), current_node, direction)

            g = child_node.depth
            f = heuristics.calculate(solved_table, child_node, heuristic) + g

            same_table_open_node = binary_search_asc(open_nodes_hash, child_node.table.hash_value)  # Index in hashcode list or None
            same_table_closed_node = utils.binary_search_asc(closed_nodes, child_node.table.hash_value)

            if same_table_open_node is None and same_table_closed_node == -1:
                # The node is reached for the 1st time, so we can easily add it
                add_to_descending_list(child_node, f, open_nodes)
                add_to_ascending_list(child_node, child_node.table.hash_value, open_nodes_hash)

            elif same_table_open_node is not None and g < same_table_open_node[0].depth:
                # We found better route to the Node
                remove_from_descending_list(child_node.table.hash_value, open_nodes)
                same_table_open_node[0] = child_node  # We have to replace Node assigned to given hash code, as it might have different e.g. depth
                add_to_descending_list(child_node, f, open_nodes)

            elif same_table_closed_node != -1:
                continue
        utils.add_to_ascending_list(closed_nodes, current_node.table.hash_value)
    return None


def search_old(solved_table, begin_table, heuristic, max_depth):
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
            g = child_node.depth
            f = heuristics.calculate(solved_table, child_node, heuristic) + g

            same_table_open_node = find_same_table_node(open_nodes, child_node.table)
            same_table_closed_node = find_same_table_node(closed_nodes, child_node.table)

            if same_table_open_node is None and same_table_closed_node is None:
                # The node is reached for the 1st time, so we can easily add it
                add_to_descending_list_old(child_node, f, open_nodes)
            elif same_table_open_node is not None and g < same_table_open_node[0].depth:
                # We found better route to the Node
                remove_from_descending_list(same_table_open_node[1], open_nodes)
                add_to_descending_list_old(child_node, f, open_nodes)
            elif same_table_closed_node is not None:
                continue

        add_to_descending_list_old(current_node, current_f, closed_nodes)
    return None


def find_same_table_node(nodes, table):
    for n in nodes:
        if n[0].table.hash_value == table.hash_value:
            return n
    return None


# Returns index of the element or -1 if not found. The list is ASCENDING
def binary_search_asc(arr, value):
    n = len(arr)
    left = 0
    right = n - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid][1] < value:
            left = mid + 1
        elif arr[mid][1] > value:
            right = mid - 1
        else:
            return arr[mid]
    return None


def add_to_ascending_list(node, value, arr):
    if len(arr) == 0 or value >= arr[-1][1]:
        arr.append([node, value])
        return

    if value <= arr[0][1]:
        arr.insert(0, [node, value])
        return

    left_pointer = 0
    right_pointer = len(arr) - 1

    while left_pointer <= right_pointer:
        mid = floor((left_pointer + right_pointer) / 2)
        if arr[mid][1] < value:
            left_pointer = mid + 1
        elif arr[mid][1] > value:
            right_pointer = mid - 1
        else:
            arr.insert(mid, [node, value])
            return

    if left_pointer > right_pointer:
        arr.insert(left_pointer, [node, value])
        return
    else:
        arr.insert(right_pointer, [node, value])
        return


def remove_from_ascending_list(arr, value):
    n = len(arr)
    left = 0
    right = n - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid][1] < value:
            left = mid + 1
        elif arr[mid][1] > value:
            right = mid - 1
        else:
            del arr[mid]
            return
    raise Exception("Value not on the list! Could not remove it!")


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


def remove_from_descending_list(value, descending_list):
    for i in range(len(descending_list)):
        if value == descending_list[i][0].table.hash_value:
            del descending_list[i]
            return
