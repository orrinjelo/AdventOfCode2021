from orrinjelo.utils.decorators import timeit

def parse(inputstr):
    dim = len(inputstr[0].strip()), len(inputstr)
    m = np.zeros(dim)
    for x in range(dim[0]):
        for y in range(dim[1]):
            m[x,y] = int(inputstr[y].strip()[x])

    return m

def calc_mimima(m):
    minima = []

    for x in range(m.shape[0]):
        for y in range(m.shape[1]):
            a = 0
            if x != 0:
                if m[x-1,y] > m[x,y]:
                    a += 1
            else:
                a += 1
            if x != m.shape[0]-1:
                if m[x+1,y] > m[x,y]:
                    a += 1
            else:
                a += 1
            if y != 0:
                if m[x,y-1] > m[x,y]:
                    a += 1
            else:
                a += 1
            if y != m.shape[1]-1:
                if m[x,y+1] > m[x,y]:
                    a += 1
            else:
                a += 1

            if a == 4:
                minima.append((int(m[x,y]), (x,y)))

    return minima    

@timeit("Day 09 Part 1")
def part1(input_str, use_rust=False):
    m = parse(input_str)

    minima = calc_mimima(m)

    risk = 0
    for x in minima:
        risk += x[0] + 1

    return risk


def bleed(x, mm):
    mm[x[0],x[1]] = True
    bled = 1
    if x[0] != 0 and mm[x[0]-1,x[1]] != True:
        bled += bleed((x[0]-1,x[1]), mm)
    if x[0] != mm.shape[0]-1 and mm[x[0]+1,x[1]] != True:
        bled += bleed((x[0]+1,x[1]), mm)
    if x[1] != 0 and mm[x[0],x[1]-1] != True:
        bled += bleed((x[0],x[1]-1), mm)
    if x[1] != mm.shape[1]-1 and mm[x[0],x[1]+1] != True:
        bled += bleed((x[0],x[1]+1), mm)
    return bled


@timeit("Day 09 Part 2")
def part2(input_str, use_rust=False):
    m = parse(input_str)
    minima = calc_mimima(m)

    counts = []

    for x in minima:
        counts.append(bleed(x[1], m==9))


    rcounts = sorted(counts, reverse=True)

    # print(rcounts)

    return rcounts[0]*rcounts[1]*rcounts[2]

# = Test ================================================

inputlist = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

def test_part1():
    assert part1(inputlist) == 15


def test_part2():
    assert part2(inputlist) == 1134

import matplotlib.pyplot as plt
import numpy as np

def plot(input_str):
    m = parse(input_str)

    plt.figure(1)
    plt.imshow(m)
    plt.figure(2)
    plt.imshow(m<9)
    plt.show()
