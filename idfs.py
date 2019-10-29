import utils
import time
import dfs


def idfs(order, solved_table, begin_table, min_limit, max_depth):
    time_before = time.time()

    # Iterative deepening DFS
    print("Inside IDFS algorithm")

    for limit in range(min_limit, max_depth):
        final_node = dfs.search(begin_table, solved_table, order, limit)
        if final_node is not None:
            print("Solution found in " + str(time.time() - time_before) + 's')

            moves = utils.create_list_of_moves(final_node)
            print("Moves to solve the puzzle: " + str(len(moves)))
            print(utils.convert_moves(moves))
            return

    print("SOLUTION NOT FOUND - REACHED MAX DEPTH")


