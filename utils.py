from math import floor

ORDER_LEFT = 0
ORDER_RIGHT = 1
ORDER_DOWN = 2
ORDER_UP = 3


def order_from_char(char):
    if char == "L" or char == "l":
        return ORDER_LEFT
    elif char == "R" or char == "r":
        return ORDER_RIGHT
    elif char == "U" or char == "u":
        return ORDER_UP
    elif char == "D" or char == "d":
        return ORDER_DOWN


def convert_moves(moves_as_ints):
    moves = list()
    arr = ["L", "R", "D", "U"]
    for move in moves_as_ints:
        moves.append(arr[move])
    return moves


def create_list_of_moves(final_node):
    moves = list()
    current_node = final_node
    while True:
        if current_node.parent is None:
            break
        moves.append(current_node.direction)
        current_node = current_node.parent

    moves.reverse()
    return moves


def binary_search(arr, value):
    n = len(arr)
    L = 0
    R = n - 1

    while L <= R:
        mid = floor((L + R) / 2)
        if arr[mid] < value:
            L = mid + 1
        elif arr[mid] > value:
            R = mid - 1
        else:
            return mid
    return -1


def add_to_ascending_list(arr, value):
    if len(arr) == 0 or value >= arr[-1]:
        arr.append(value)
        return

    if value <= arr[0]:
        arr.insert(0, value)
        return

    left_pointer = 0
    right_pointer = len(arr) - 1

    while left_pointer <= right_pointer:
        mid = floor((left_pointer + right_pointer) / 2)
        if arr[mid] < value:
            left_pointer = mid + 1
        elif arr[mid] > value:
            right_pointer = mid - 1
        else:
            arr.insert(mid, value)

    if left_pointer > right_pointer:
        arr.insert(left_pointer, value)
    else:
        arr.insert(right_pointer, value)
