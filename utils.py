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


def reverse_move(move):
    if move == ORDER_LEFT:
        return ORDER_RIGHT
    elif move == ORDER_RIGHT:
        return ORDER_LEFT
    elif move == ORDER_DOWN:
        return ORDER_UP
    elif move == ORDER_UP:
        return ORDER_DOWN


def convert_moves(moves_as_ints):
    moves = ""
    arr = ["L", "R", "D", "U"]
    for i in range(len(moves_as_ints)):
        moves += arr[moves_as_ints[i]]
        if i < len(moves_as_ints) - 1:
            moves += ","
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


# Returns index of the element or -1 if not found. The list is ASCENDING
def binary_search_asc(arr, value):
    n = len(arr)
    left = 0
    right = n - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid] < value:
            left = mid + 1
        elif arr[mid] > value:
            right = mid - 1
        else:
            return mid
    return -1


# Returns index of the element or -1 if not found. The list is DESCENDING
def binary_search_desc(arr, value):
    n = len(arr)
    left = 0
    right = n - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid] < value:
            right = mid - 1
        elif arr[mid] > value:
            left = mid + 1
        else:
            return mid
    return -1


def remove_from_descending_list(arr, value):
    n = len(arr)
    left = 0
    right = n - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid] < value:
            right = mid - 1
        elif arr[mid] > value:
            left = mid + 1
        else:
            del arr[mid]
            return
    raise Exception("Value not on the list! Could not remove it!")


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
            return

    if left_pointer > right_pointer:
        arr.insert(left_pointer, value)
        return
    else:
        arr.insert(right_pointer, value)
        return


def process_table_input(rows, columns):
    print("Pass the input")

    input_table = [[0 for x in range(rows)] for y in range(columns)]

    for row in range(rows):
        raw_line = input()
        elements = raw_line.split()
        max_value = rows * columns - 1

        if len(elements) != columns:
            raise Exception("ERROR, columns and input doesnt match")
        for i in range(len(elements)):
            value = int(elements[i])
            if value > max_value:
                raise Exception("ERROR, value out of possible range: <0:" + str(max_value)+">")
            input_table[row][i] = value

    # Used to check if the numbers are fine
    validation_list = [False] * (rows * columns)

    for row in range(rows):
        for column in range(columns):
            validation_list[input_table[row][column]] = True

    for b in validation_list:
        if not b:
            raise Exception("ERROR, INCORRECT NUMBERS", validation_list)

    return input_table


def add_to_decending_list(arr, value):
    if len(arr) == 0 or value <= arr[-1]:
        arr.append(value)
        return

    if value >= arr[0]:
        arr.insert(0, value)
        return

    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = floor((left + right) / 2)
        if arr[mid] < value:
            right = mid - 1
        elif arr[mid] > value:
            left = mid + 1
        else:
            arr.insert(mid, value)
            return

    if left > right:
        arr.insert(left, value)
        return
    else:
        arr.insert(right, value)
        return