from orrinjelo.utils.decorators import timeit
import numpy as np
import sys
import re

def parse_lines(instr):
    pl = re.compile(r'target area: x=(\-?\d+)\.\.(\-?\d+), y=(\-?\d+)\.\.(\-?\d+)')
    matches = pl.match(instr)
    x_min, x_max, y_min, y_max = matches.groups()

    return (int(x_min), int(x_max)), (int(y_min), int(y_max))

def signum(x):
    return 1 if x >= 0 else -1

# Eqns: 
#  x[i+1] = x[i] + vx[i]
#  vx[i+1] = vx[i] - signum(vx[i])
#  y[i+1] = y[i] + vy[i]
#  yx[i+1] = yx[i] - 1  
def step(x, y, vx, vy):
    x += vx
    y += vy
    vx -= signum(x)
    vy -= 1
    return x, y, vx, vy

def hit_target(tx, ty):
    x, y = 0, 0

    # Eqns:
    # s = ut + 1/2at^2
    # t = -ux +/- sqrt(ux^2 + 2*a*x) = -uy +/- sqrt(uy^2 + 2*a*y)
    # u ~= sqrt(2y)
    ux = int(np.sqrt(2*tx[0])+1), int(np.sqrt(2*tx[1]))
    t = ux[0] - np.sqrt(ux[0]**2 - 2*tx[0]), ux[1] - np.sqrt(ux[1]**2 - 2*tx[0])
    print(t)

@timeit("Day 17 Part 1")
def part1(input_str, use_rust=False):
    x, y = parse_lines(input_str)
    print(x[0], x[1])
    ux = np.sqrt(2*x[0]), np.sqrt(2*x[1])
    hit_target(x,y)

    return ux

@timeit("Day 17 Part 2")
def part2(input_str, use_rust=False):
    m = parse_lines(input_str)
    return 0



# = Test ================================================

inputlist1 = [
    'target area: x=20..30, y=-10..-5',
]


def test_part1():
    assert part1(inputlist1) == (6,9), 45

def test_part2():
    assert part2(inputlist1) == 0

# import pygame
# import sys
# from pygame import gfxdraw


def plot(input_str):
    pass