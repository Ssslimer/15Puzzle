HAMMING_DISTANCE = 0
MANHATTAN_DISTANCE = 1
WEIGHTED_HAMMING = 2


def calculate(solved_table, node, heuristics=0):
    if heuristics == HAMMING_DISTANCE:
        return __hamming_heuristic(solved_table, node)
    elif heuristics == MANHATTAN_DISTANCE:
        return __manhattan_heuristic(solved_table, node)
    elif heuristics == WEIGHTED_HAMMING:
        return __weighted_hamming_heuristic(solved_table, node)


def __hamming_heuristic(solved_table, node):
    return node.table.count_wrong_puzzles(solved_table)


def __manhattan_heuristic(solved_table, node):
    manhattan_distance_sum = 0

    for row in range(len(solved_table.data)):
        for column in range(len(solved_table.data[row])):
            value = solved_table.data[row][column]
            actual_row, actual_column = node.table.find_value(value)
            manhattan_distance_sum += abs(actual_row - row) + abs(actual_column - column)

    return manhattan_distance_sum


def __weighted_hamming_heuristic(solved_table, node):
    weighted_sum = 0
    for row in range(node.table.rows):
        for column in range(node.table.columns):
            if node.table.data[row][column] != solved_table.data[row][column]:
                if column < row:
                    weighted_sum += node.table.columns - column
                else:
                    weighted_sum += node.table.rows - row

    return weighted_sum