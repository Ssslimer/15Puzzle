from math import floor

import heuristics
import utils
from node import Node


def search(solved_table, begin_table, heuristic, max_depth, max_memory):
    open_nodes = [[Node(begin_table), 0]]  # Node, f(n) GIT
    open_nodes_hash = [[open_nodes[0][0], open_nodes[0][0].table.hash_value]]  # [Node, Node.table.hashcode]
    closed_nodes = list()  # hashcodes GIT

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
                removed_elements_array = add_to_descending_list(child_node, f, open_nodes, max_memory)
                add_to_ascending_list(child_node, child_node.table.hash_value, open_nodes_hash, max_memory)

                # Check correctness!!!!!!!!!!!!!!!!!!!!!!!!!!1
                remove_hash_values_from_deleted_nodes(open_nodes_hash, removed_elements_array)

            elif same_table_open_node is not None and g < same_table_open_node[0].depth:
                # We found better route to the Node
                remove_from_descending_list(child_node.table.hash_value, open_nodes)  # NOT GUT, optimize
                same_table_open_node[0] = child_node  # We have to replace Node assigned to given hash code, as it might have different e.g. depth
                add_to_descending_list(child_node, f, open_nodes, max_memory)

                # no adding to hash table here, so no removing hash values, right?

            elif same_table_closed_node != -1:
                continue
        utils.add_to_ascending_list(closed_nodes, current_node.table.hash_value)
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


def add_to_ascending_list(node, value, arr, max_memory):
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


def add_to_descending_list(node, value, arr, max_memory):
    if len(arr) == 0 or value <= arr[-1][1]:
        arr.append([node, value])
        return None

    if value >= arr[0][1]:
        arr.insert(0, [node, value])
        return None

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
            return remove_worst_elements(arr, False, max_memory)

    if left > right:
        arr.insert(left, [node, value])
        return remove_worst_elements(arr, False, max_memory)
    else:
        arr.insert(right, [node, value])
        return remove_worst_elements(arr, False, max_memory)


def remove_hash_values_from_deleted_nodes(hash_array, deleted_array):
    index = 0

    if deleted_array is None:
        return

    while index < len(deleted_array):
        value_of_node = deleted_array[index][0].table.hash_value

        hash_array_index = 0

        while hash_array_index < len(hash_array):
            # check if this is correct way of accessing hash array!!!!!!!!!!!!!!!!!!!
            if hash_array[hash_array_index] == value_of_node:
                del hash_array[hash_array_index]
            hash_array_index += 1

        index += 1

    return


def remove_worst_elements(arr, is_ascending, max_memory):
    deleted_array = []

    if len(arr) < max_memory:
        return

    if is_ascending:
        index = 0

        while len(arr) > max_memory and index < len(arr):
            deleted_array.append(arr[index])
            del arr[index]
            index += 1

    else:
        index = len(arr) - 1

        while len(arr) > max_memory and index >= 0:
            deleted_array.append(arr[index])
            del arr[index]
            index -= 1

    return deleted_array


def remove_from_descending_list(value, descending_list):
    for i in range(len(descending_list)):
        if value == descending_list[i][0].table.hash_value:
            del descending_list[i]
            return
