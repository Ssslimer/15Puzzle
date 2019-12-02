import dfs


def search(order, solved_table, begin_table, min_limit, max_depth):
    for limit in range(min_limit, max_depth+1):
        print("New depth limit:" + str(limit))
        final_node = dfs.search(begin_table=begin_table, solved_table=solved_table, order=order, max_depth=limit, random_orders=order is None)
        if final_node is not None:
            return final_node

    return None
