#!/usr/bin/env python3

'''
Sample space: 
All possible permutations of the numbers of the 4 x 4 board

Initial state: 
The initial state is the the board that we have been provided as the input

Edge cost: 
The edge cost in this case is 1. As each transistion is one move.

Successor function: 
The successor function returns all the possible moves possible from the current state.
To get the next state we can move any one of the row either left or right or we can move a column 
up or down.
The succesor function gives all such possible next states.


Search strategy: 
In the starter code provided a BFS algorithm was used. 
This strategy does give us optimal answer for board2 and board4. 

However it is too slow for board6 and results in a memory error for board6

This is because BFS is a blind search. 
The performance can be improved by using a astar search instead. 

For astar I evaluated various heuristics: 

1. Manhattan distance: 
This does not take into consideration that there is a wrap possible. 
Admissible : NO 
Consistent : NO

2. Manhattan distance with wrap:
This does not take into consideration that in one move there will be 4 elements which actually move.
Admissible : NO 
Consistent : NO

3. Out of place blocks/4 
Calaculated the out of place blocks and divided it by 4. 
Admissible : YES
Consistent : YES

However, it was too slow and resulted in memory error 

4. Manhattan distance with wrap / 4 : 
In order to handle the shortcoming of the previous heuristic, I divided the Manhattan dist by 4
Admissible : YES 
Consistent : YES

This does find the optimal solution for board6, however it is too slow for board 12 and results in memory
error. 

5. Custom heuristic function. 

The above heuristic was admissible and consistent but wan't providing enough information for the search
and hence was slow. In order to provide more information I create my own heuristic with some modifications

1. Found x and y out of place distance seperately considering the wrap for each number.
2. Now I traverse each row in goal state and find the maximum horizontally out of place
element distance in them and add it up.
3. Repeat the above step for the columns as well and find the maximum vertically out of place
element. 

Admissible : YES 
Consistent : YES

For each row and column we will need atleast the maximum number of moves to solve the board. 
Hence, this function is both admissible and consistent. 

This function takes a Maximum and hence, gives a tighter bound.

This heuristic was able to solve the board12 as well as the board15 (provided by Prof Crandall on Piazza)

The following results were obtained by using this heuristic function on burrow server: 

board2  0m0.081s
board4  0m0.085s  
board6  0m0.108s
board12 0m8.231s
board15 0m42.085s
'''

from queue import PriorityQueue
from random import randrange, sample
import sys
import string
import time

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return (state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j+4)]))

# Manhattan distance divided by 4
def heuristics2(state):
    value = 0
    for pos, element in enumerate(state):
        row = (element-1)//4
        col = (element-1)%4
        row_current = pos//4 
        col_current = pos%4
        x = abs(row_current - row)
        
        # considering the wrap situation
        if x == 3:
            x = 1

        y = abs(col_current - col)
        if y == 3:
            y = 1
        
        value+= (x+y)
    return(value//4)


# custom heuristic function
def heuristics3(state):
    value = 0

    points = {}
    for pos, element in enumerate(state):
        row = (element-1)//4
        col = (element-1)%4
        row_current = pos//4 
        col_current = pos%4
        x = abs(row_current - row)
        if x == 3:
            x = 1

        y = abs(col_current - col)
        if y == 3:
            y = 1
        
        # store the x and y distance for each element    
        points[(row, col)] = (x,y) 
    
    total = 0

    # find maximum out of place distance for each row and add them up
    for row in range(4):
        maxi = 0
        for col in range(4):
            x , y = points[(row,col)]
            maxi = max(maxi, y)
        total+=maxi

    # find maximum out of place distance for each column and add them up
    for col in range(4):
        maxi = 0
        for row in range(4):
            x , y = points[(row,col)]
            maxi = max(maxi, x)
        total+=maxi    
    return(total)

# out of place elements divided by 4
def heuristics(state):
    value = 0
    for pos, element in enumerate(state):
        row = (element-1)//4
        col = (element-1)%4
        row_current = pos//4 
        col_current = pos%4
        
        if(row != row_current or col != col_current):
            value+=1
    return(value//4)

# return a list of possible successor states
def successors(state):
    succ = [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 
    succ_result = []
    for state, move in succ:
        heuristic = heuristics3(state)
        succ_result.append((state, move, heuristic))
    return succ_result

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)
    
# The solver! - using BFS right now
def solve(initial_board):
    visited = {}
    fringe = PriorityQueue()
    fringe.put((1,(initial_board, "")))
    while fringe.qsize() > 0:
        (priority, (state,route_so_far)) = fringe.get()
        for (succ, move, heuristic) in successors(state):
            if is_goal(succ):
                return( route_so_far + " " + move )
            if succ not in visited:
                visited[succ] = True
                length = len(route_so_far.split())
                fringe.put((heuristic+length, (succ, route_so_far + " " + move )))
    
    return False


start_state = []
file_name = str(sys.argv[1])

with open(file_name, 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

start = time.time()

print("Start state: ")
print_board(tuple(start_state))
print("Solving...")
route = solve(tuple(start_state))

print("Solution found in " + str(len(route)/3) + " moves:" + "\n" + route)
