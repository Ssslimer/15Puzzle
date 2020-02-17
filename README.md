**15Puzzle**
==========
The project was done for unviersity Artificial Inteligence and Expert Systems course
-----------
**The given problem of finding solution to solve the puzzle had to be achieved with different strategies**:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- IDDFS (Iterative Deepening Depth-First Search)
- Best-first search
- A*
- SMA* (Simplified Memory Bounded A*)
-----------
**Some search algorithms require an additional heuristcs to work. The following has been implemented:**
- Hamming distance
- Manhattan distance
- Hamming distance with weights

Input
============
In the first line of standard input two integer values R C are given: , row count and column count respectively, defining frame size. In each subsequent R lines of standard input contains C space separated integer values describing a piece in the puzzle. Value 0 denotes empty space in the given frame.

Output
=========
If the solution was found a list of moves is returned

Viewer
==========
An additional program to visualize process of solving a puzzle step by step
