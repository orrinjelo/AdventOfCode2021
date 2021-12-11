from orrinjelo.utils.decorators import timeit
import numpy as np

def parse(lines):
    return np.array([[int(c) for c in line.strip()] for line in lines])

visited = []
def flash(a, x, y):
    global visited
    if (x,y) in visited:
        return
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx == 0 and dy == 0:
                continue
            if x+dx < 0 or x+dx >= a.shape[0]:
                continue
            if y+dy < 0 or y+dy >= a.shape[1]:
                continue
            a[x+dx, y+dy] += 1
            visited.append((x,y))
            if a[x+dx, y+dy] > 9:
                flash(a, x+dx, y+dy)

def progress(a):
    global visited
    a += 1

    x,y = np.where(a > 9)
    visited = []
    for i in range(len(x)):
        flash(a,x[i],y[i])

    count = np.sum(a > 9)
    # print('a:\n', a)

    a[a > 9] = 0

    return a, count

@timeit("Day 11 Part 1")
def part1(input_str, use_rust=False):
    octomap = parse(input_str)
    total_count = 0

    for i in range(100):
        octomap, count = progress(octomap)
        total_count += count

    return total_count

@timeit("Day 11 Part 2")
def part2(input_str, use_rust=False):
    octomap = parse(input_str)
    step = 0
    while True:
        step += 1
        octomap, count = progress(octomap)
        if count == octomap.shape[0]*octomap.shape[1]:
            break

    return step


# = Test ================================================

inputlist = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]

def test_part1():
    # import matplotlib.pyplot as plt
    # plt.imshow(parse(inputlist))
    # plt.show()
    
    assert part1(inputlist) == 1656


def test_part2():
    assert part2(inputlist) == 195

import pygame
import sys


def plot(input_str):
    # octomap = parse(input_str)
    octomap = np.random.randint(0,9,(100,100))

    pygame.init()
    clock = pygame.time.Clock()

    scale = 5

    screen = pygame.display.set_mode((octomap.shape[0]*scale,octomap.shape[1]*scale))
    surface = pygame.Surface((octomap.shape[0]*scale,octomap.shape[1]*scale))

    frame = 0

    history = []
    for i in range(500):
        print('Generating frame #', i)
        octomap, _ = progress(octomap)
        history.append(np.copy(octomap))
    input()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();

        # erase the screen
        screen.fill((255,0,0))

        try:
            octomap = history[frame]
        except:
            frame = 0

        for i in range(octomap.shape[0]):
            for j in range(octomap.shape[1]):
                if octomap[i,j] == 0:
                    brightness = 255
                else:
                    brightness = int(255.0 * octomap[i,j]/10.0)

                print(i*scale, j*scale, brightness)
                pygame.draw.rect(
                    screen, 
                    (brightness,brightness,brightness),
                    pygame.Rect(i*scale, j*scale, scale, scale)
                )

        pygame.display.update()
        # surface.blit(screen, (0,0))

        clock.tick(30)
        frame += 1