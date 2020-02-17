**15Puzzle**
==========
The project was done for unviersity Artificial Inteligence and Expert Systems course
-----------
The given problem of finding solution to solve the puzzle had to be achieved with different strategies:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- IDDFS (Iterative Deepening Depth-First Search)
- Best-first search
- A*
- SMA* (Simplified Memory Bounded A*)

-----------

Informed search strategies must be tested using at least 2 heuristics. Additionally they should be teted with h(x)=0 heuristic.
Functional requirements

It is expected from each group to present two programs. The first one, verifiable in linux/unix environment, reads initial state of a puzzle from standard input and on standard output presents the solution found - sequence of actions solving the puzzle. It is assumed, that letter 'L' denotes a move of a piece having freedom to the left, R to the right, U up, and D down. The program must be parametrised using following command line arguments.
Command line arguments:
  	

	-b/--bfs order 	Breadth-first search

	-d/--dfs order 	Depth-first search

	-i/--idfs order 	Iterative deepenening DFS

	-h/--bf id_of_heurisic 	Best-first strategy

	-a/--astar id_of_heurisic 	A* strategy

	-s/--sma id_of_heurisic 	SMA* strategy

Where order is a permutation of a set {'L','R','U','D'} defining an order in which successors of given state are processed, e.g. string DULR means the following search order: down, up, left, right. If order starts with 'R' it should be random (each node has random neighborhood search order).

Input
============
In the first line of standard input two integer values R C are given: , row count and column count respectively, defining frame size. In each subsequent R lines of standard input contains C space separated integer values describing a piece in the puzzle. Value 0 denotes empty space in the given frame.

Output
=========
Standard output of a given program should consist of at least two lines. The first line should contain one value n: the length of the solution found by the program or -1 if puzzle has not been solved. Second line of standard output should be a string of length n containing uppercase latin characters from set {'L','R', 'U', 'D'} describing the solution. If the solution does not exist the second line should be empty.

**Viewer**
==========
Student are also required to present a second application that allows to view previously found solution step by step (with jumps).
