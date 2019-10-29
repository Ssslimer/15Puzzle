from node import Node
from random import shuffle
import table
import utils

import dfs


def idfs(order, solved_table, begin_table, min_limit, max_depth):

    # Iterative deepening DFS
    print("Inside IDFS algorithm")

    final_node = dfs.search(begin_table, solved_table, order)

    if final_node is None:
        print("SOLUTION NOT FOUND - REACHED MAX DEPTH")
    else:
        print("SOLUTION FOUND")


