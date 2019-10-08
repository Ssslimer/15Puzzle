import sys
from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star

def determine_method():
    if sys.argv[1] == "-b" or sys.argv[1] == "-bfs":
        return 0
    elif sys.argv[1] == "-d" or sys.argv[1] == "-dfs":
        return 1
    elif sys.argv[1] == "-i" or sys.argv[1] == "-idfs":
        return 2
    elif sys.argv[1] == "-h" or sys.argv[1] == "-bf":
        return 3
    elif sys.argv[1] == "-a" or sys.argv[1] == "-astar":
        return 4
    elif sys.argv[1] == "-s" or sys.argv[1] == "-sma":
        return 5
    else:
        return -1

def call_algorithm(method):
    if method == 0:
        bfs()
    elif method == 1:
        dfs()
    elif method == 2:
        idfs()
    elif method == 3:
        best_first_search()
    elif method == 4:
        a_star()
    elif method ==  5:
        sma_star()



def main(argv):
    method = determine_method()

    if method == -1:
        print("No algorithm was chosen, please try again")
        return

    call_algorithm(method)






main(sys.argv[1:])
