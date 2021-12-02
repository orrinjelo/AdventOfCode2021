from orrinjelo.utils.decorators import timeit
from orrinjelo.aoc2021.rust.pyaoc import day02_part1, day02_part2

@timeit("Day 02 Part 1")
def part1(instructions, use_rust=False):
    if use_rust:
        return day02_part1(instructions)

    pos = (0, 0) # X, Y

    for line in instructions:
        direction, dist = line.strip().split()
        dist = int(dist)

        if direction == 'forward':
            pos = (pos[0]+dist, pos[1])
        elif direction == 'up':
            pos = (pos[0], pos[1]-dist)
        elif direction == 'down':
            pos = (pos[0], pos[1]+dist)

    return pos[0]*pos[1]

@timeit("Day 02 Part 2")
def part2(instructions, use_rust=False):
    if use_rust:
        return day02_part2(instructions)


    pos = (0, 0) # horiz, depth
    aim = 0

    for line in instructions:
        direction, dist = line.strip().split()
        dist = int(dist)

        if direction == 'forward':
            pos = (pos[0]+dist, pos[1]+dist*aim)
        elif direction == 'up':
            aim -= dist
        elif direction == 'down':
            aim += dist

    return pos[0]*pos[1]

def test_part1():
    inp = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    assert part1(inp) == 150

def test_part2():
    inp = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    assert part2(inp) == 900

def plot(instructions):

    pos = (0, 0) # X, Y
    pos2 = (0, 0) # X, Y
    aim = 0

    pos_hist = []
    pos2_hist = []

    for line in instructions:
        direction, dist = line.strip().split()
        dist = int(dist)

        if direction == 'forward':
            pos = (pos[0]+dist, pos[1])
            pos2 = (pos2[0]+dist, pos2[1]+dist*aim)
        elif direction == 'up':
            pos = (pos[0], pos[1]-dist)
            aim -= dist
        elif direction == 'down':
            pos = (pos[0], pos[1]+dist)
            aim += dist

        pos_hist.append(pos)
        pos2_hist.append(pos2)

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.title('Submarine Charted Path')
    plt.plot([x[0] for x in pos_hist], [x[1] for x in pos_hist], color='blue', label='incorrect pathing')
    plt.plot([x[0] for x in pos2_hist], [x[1] for x in pos2_hist], color='red', label='corrected pathing')
    # plt.plot([0.001 for _ in range(pos_hist[-1][0])], 'k--', label='sea level')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.yscale("log")
    plt.xlabel('Horizontal distance (arb.)')
    plt.ylabel('Depth (arb.)')
    plt.show()
