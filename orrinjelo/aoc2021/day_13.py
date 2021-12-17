from orrinjelo.utils.decorators import timeit
import matplotlib.pyplot as plt
import numpy as np
import sys

def parse_lines(lines):
    instructions = False
    coords = []
    folds = []
    for line in lines:
        if not instructions:
            if line.strip() == '':
                instructions = True
                continue
            coords.append(tuple([int(x) for x in line.strip().split(',')]))
        else:
            parts = line[11:].split('=')
            axis, val = parts[0], int(parts[1])
            folds.append(tuple([axis, val]))

    return coords, folds

def make_map(coords):
    max_x, max_y = 0,0
    for c in coords:
        if c[0] > max_x:
            max_x = c[0]
        if c[1] > max_y:
            max_y = c[1]
    m = np.zeros((max_x+1, max_y+1), dtype=bool)

    for c in coords:
        m[c[0],c[1]] = True

    return m

def fold_map(m, fold):
    axis, val = fold
    if axis == 'x':
        for x in range(val):
            m[x, :] |= m[m.shape[0]-x-1,:]

        mm = np.array(m[:val, :])
    else:
        for y in range(val):
            m[:, y] |= m[:,m.shape[1]-y-1]
        mm = np.array(m[:, :val])
    return mm


@timeit("Day 13 Part 1")
def part1(input_str, use_rust=False):
    coords, folds = parse_lines(input_str)
    m = make_map(coords)
    m = fold_map(m, folds[0])
    # for fold in folds:
    #     m = fold_map(m, fold)

    return np.sum(m)


@timeit("Day 13 Part 2")
def part2(input_str, use_rust=False):
    coords, folds = parse_lines(input_str)
    m = make_map(coords)
    for fold in folds:
        m = fold_map(m, fold)

    # plt.figure()
    # plt.imshow(np.transpose(m))
    # plt.show()


    return 0



# = Test ================================================

inputlist1 = [
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5',
]

def test_part1():
    coords, folds = parse_lines(inputlist1)

    assert coords == [(6,10),(0,14),(9,10),(0,3),(10,4),(4,11),
        (6,0),(6,12),(4,1),(0,13),(10,12),(3,4),(3,0),(8,4),(1,10),(2,14),(8,10),(9,0)]
    
    assert folds == [('y',7),('x',5)]

    assert part1(inputlist1) == 17

    # m = make_map(coords)
    # # plt.imshow(np.transpose(m))
    # # plt.show()
    # m = fold_map(m, folds[0])
    # m = fold_map(m, folds[1])
    
    # plt.imshow(np.transpose(m))
    # plt.show()


def test_part2():
    pass

import pygame
import sys
from pygame import gfxdraw

def draw_pill(surface, color, x, y, scale=1):
    # surface.set_at((x, y), color)
    rectobj = pygame.Rect(x*scale, y*scale, scale, scale)
    # print(rectobj
    pygame.draw.rect(surface, color, rectobj)


def plot(input_str):
    coords, folds = parse_lines(input_str)
    m = make_map(coords)

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((600,600))
    surface = pygame.Surface((600,600))

    input()
    frame = 0
    step = 0

    steps = [m.copy()]

    for fold in folds:
        m = fold_map(m, fold)
        steps.append(m.copy())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();

        # erase the screen
        screen.fill((255, 255, 255))

        try:
            coords = np.where(steps[frame])
            # print(coords)

            for i in range(len(coords[0])):
                draw_pill(screen, (0, 0, 255), coords[0][i], coords[1][i], frame//2)

            # for j in range(1000):
            #     surface.set_at((j, j), (0, 0, 0))
            #     gfxdraw.pixel(screen, j, j, (0,0,0))

            pygame.display.update()
            surface.blit(screen, (0,0))        

            clock.tick(0.5)
            frame += 1
        except Exception as e:
            pass