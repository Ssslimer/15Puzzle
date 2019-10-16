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
        moves.append(current_node.direction)
        if current_node.parent is None:
            break
        current_node = current_node.parent

    moves.reverse()
    return moves
