from orrinjelo.utils.decorators import timeit
import numpy as np
import sys

def parse_lines(instr):
    shape = len(instr), len(instr[0].strip())
    m = np.zeros(shape, dtype=int)
    for l in range(shape[0]):
        for c in range(shape[1]):
            m[l,c] = instr[l].strip()[c]
    return m        

# def recursive_step(m, x=0, y=0, history=[]):
#     # Slow
#     history.append(m[x,y])
#     right = None
#     down = None
#     if x == m.shape[0] - 1 and y == m.shape[1] - 1:
#         return sum(history[1:])
#     if x < m.shape[0] - 1:
#         right = recursive_step(m, x+1, y, history[:])
#     if y < m.shape[1] - 1:
#         down = recursive_step(m, x, y+1, history[:])

#     if right and down:
#         if right < down:
#             return right
#         else:
#             return down
#     elif right:
#         return right
#     else:
#         return down

# def backtrack_count(m, x=None, y=None, h=None):
#     if x == 0 and y == 0:
#         return
#     if h is None:
#         h = np.zeros_like(m, dtype=int)
#     if x is None and y is None:
#         x,y = m.shape[0]-1,m.shape[1]-1
#     # Cast up
#     if y != 0:
#         if h[x,y-1] == 0 or h[x,y-1] > m[x,y] + h[x,y]:
#             h[x,y-1] = m[x,y] + h[x,y]

#     # Cast left
#     if x != 0:
#         if h[x-1,y] == 0 or h[x-1,y] > m[x,y] + h[x,y]:
#             h[x-1,y] = m[x,y] + h[x,y]

#     if y != 0:
#         backtrack_count(m, x, y-1, h)
#     if x != 0:
#         backtrack_count(m, x-1, y, h)
    
#     return h[0,0]

# def minCost(cost, x, y):
#     if (y < 0 or x < 0):
#         return sys.maxsize
#     elif (x == 0 and y == 0):
#         return cost[x,y]
#     else:
#         return cost[x,y] + min( [#minCost(cost, x-1, y-1),
#                                  minCost(cost, x-1, y),
#                                  minCost(cost, x, y-1)] ) 

def increase_risk(mm, i):
    mm += i
    mm[mm > 9] %= 9
    return mm

def extend_cave(m):
    mm = m.copy()
    # Extend down
    for i in range(1,5):
        mm = np.append(mm, increase_risk(m.copy(), i), axis=0)
    mmm = mm.copy()
    for i in range(1,5):
        mmm = np.append(mmm, increase_risk(mm.copy(), i), axis=1)

    return mmm

def find_path(m):
    solution = np.zeros_like(m, dtype=int)
    g = np.zeros(m.shape)

    solution[0,0] = m[0,0]
    # fill the first row
    for i in range(1, m.shape[1]):
        solution[0,i] = m[0,i] + solution[0,i-1]

    # fill the first column
    for i in range(1, m.shape[0]):
        solution[i,0] = m[i,0] + solution[i-1,0]

    for i in range(1, m.shape[0]):
        for j in range(1, m.shape[1]):
            solution[i,j] = m[i,j] + min(solution[i-1,j], solution[i,j-1])
            if solution[i-1,j] < solution[i,j-1]:
                g[i-1,j] += 1
            else:
                g[i,j-1] += 1

    return solution[-1,-1] - m[0,0], g
 

@timeit("Day 14 Part 1")
def part1(input_str, use_rust=False):
    m = parse_lines(input_str)
    # return recursive_step(m)
    # return backtrack_count(m)
    # return minCost(m.copy(), m.shape[0]-1, m.shape[1]-1) - m[0,0]
    return find_path(m)[0]

@timeit("Day 14 Part 2")
def part2(input_str, use_rust=False):
    m = parse_lines(input_str)
    mm = extend_cave(m)

    path, hist = find_path(mm)

    
    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.imshow(mm)
    # plt.figure(2)
    # plt.imshow(hist)
    plt.show()
    
    return path



# = Test ================================================

inputlist1 = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]

inputlist2 = [
    '0010',
    '1011',
    '1001',
    '1100'
]

def test_part1():
    assert part1(inputlist1) == 40

def test_part2():
    assert part2(inputlist1) == 315
    assert part2(inputlist2) == 156

# import pygame
# import sys
# from pygame import gfxdraw


def plot(input_str):
    pass