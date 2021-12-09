from orrinjelo.utils.decorators import timeit

@timeit("Day 07 Part 1")
def part1(input_str, use_rust=False):
    crabs = [int(x) for x in input_str.strip().split(',')]
    minp, maxp = min(crabs), max(crabs)
    distances = {}
    for pos in range(minp, maxp+1):
        dist = 0
        for crab in crabs:
            dist += abs(crab - pos)
        distances[pos] = dist

    shortest = min(distances, key=distances.get)
    goal = distances[shortest]

    return shortest, goal

# 1, 3, 6, 10 - These are triangular numbers!
@timeit("Day 07 Part 2")
def part2(input_str, use_rust=False):
    crabs = [int(x) for x in input_str.strip().split(',')]
    print(f"Mean: {sum(crabs)/len(crabs)}")
    minp, maxp = min(crabs), max(crabs)
    distances = {}
    for pos in range(minp, maxp+1):
        dist = 0
        for crab in crabs:
            n = abs(crab - pos)
            dist += n*(n+1)//2
            # if pos == 5: print(f'Move from {crab} to {pos}: {n*(n+1)//2}')
        distances[pos] = dist

    # print(distances)

    shortest = min(distances, key=distances.get)
    goal = distances[shortest]

    return shortest, goal

def test_part1():
    assert part1('16,1,2,0,4,2,7,1,2,14') == (2, 37)

def test_part2():
    assert part2('16,1,2,0,4,2,7,1,2,14') == (5, 168)

def plot(input_str):
    crabs = [int(x) for x in input_str.strip().split(',')]
    minp, maxp = min(crabs), max(crabs)
    import matplotlib.pyplot as plt
    import numpy as np
    grid = np.zeros((maxp-minp+1, maxp-minp+1))
    for pos in range(minp, maxp+1):
        for crab in crabs:
            n = abs(crab - pos)
            grid[crab, pos] = n*(n+1)//2

    plt.figure(1)
    plt.ylabel('Crab Starting Position')
    plt.xlabel('Destination Position')
    plt.imshow(grid, cmap='gnuplot')
    plt.colorbar()
    plt.show()