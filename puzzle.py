import sys
from bfs import bfs
from dfs import dfs
from idfs import idfs
from best_first_search import best_first_search
from a_star import a_star
from sma_star import sma_star

def main(argv):
    if sys.argv[1] == "-b" or sys.argv[1] == "-bfs":
        print("BFS")
        bfs()
    elif sys.argv[1] == "-d" or sys.argv[1] == "-dfs":
        print("DFS")
        dfs()
    elif sys.argv[1] == "-i" or sys.argv[1] == "-idfs":
        print("IDFS")
        idfs()
    elif sys.argv[1] == "-h" or sys.argv[1] == "-bf":
        print("Best first search")
        best_first_search()
    elif sys.argv[1] == "-a" or sys.argv[1] == "-astar":
        print("A*")
        a_star()
    elif sys.argv[1] == "-s" or sys.argv[1] == "-sma":
        print("SMA*")
        sma_star()
    else:
        print("No algorithm was chosen, please try again")




main(sys.argv[1:])
