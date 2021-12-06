from orrinjelo.utils.decorators import timeit

import numpy as np
import matplotlib.pyplot as plt

def parse(input_str):
    parts = input_str.split('->')
    x1, y1 = (int(x) for x in parts[0].strip().split(','))
    x2, y2 = (int(x) for x in parts[1].strip().split(','))

    return x1, y1, x2, y2

@timeit("Day 05 Part 1")
def part1(input_str, use_rust=False):
    grid = np.zeros((1000, 1000))

    for line in input_str:
        x1, y1, x2, y2 = parse(line)
        if not (x1 == x2 or y1 == y2):
            continue

        if x1 > x2:
            temp = x2
            x2 = x1
            x1 = temp
        if y1 > y2:
            temp = y2 
            y2 = y1 
            y1 = temp

        grid[x1:x2+1, y1:y2+1] += 1 

    crosses = np.where(grid >= 2)

    return len(crosses[0])

@timeit("Day 05 Part 2")
def part2(input_str, use_rust=False):
    grid = np.zeros((1000, 1000))

    for line in input_str:
        x1, y1, x2, y2 = parse(line)

        dx = 1 if x2 > x1 else -1 if x1 > x2 else 0
        dy = 1 if y2 > y1 else -1 if y1 > y2 else 0
        for i in range(max(abs(x2 - x1), abs(y2 - y1))+1):
            grid[x1+i*dx, y1+i*dy] += 1

    crosses = np.where(grid >= 2)

    return len(crosses[0])


# = Testing ==========================
test_str = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]

def test_part1():
    assert parse(test_str[0]) == (0, 9, 5, 9)

    assert part1(test_str) == 5

def test_part2():
    assert part2(test_str) == 12

def plot(input_str):
    grid = np.zeros((1000, 1000))

    for line in input_str:
        x1, y1, x2, y2 = parse(line)

        dx = 1 if x2 > x1 else -1 if x1 > x2 else 0
        dy = 1 if y2 > y1 else -1 if y1 > y2 else 0
        for i in range(max(abs(x2 - x1), abs(y2 - y1))+1):
            grid[(x1+i*dx), (y1+i*dy)] += 1

    plt.figure(1)
    plt.imshow(np.transpose(grid), cmap='viridis')
    plt.figure(2)
    plt.imshow(np.transpose(grid >= 2))
    plt.show()