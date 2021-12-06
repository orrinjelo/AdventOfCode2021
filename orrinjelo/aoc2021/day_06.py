from orrinjelo.utils.decorators import timeit

from pprint import pprint

class Pool():
    contents = {
        k: 0 for k in range(9)
    }

    history = []

    @staticmethod
    def day():
        Pool.contents[9] = 0
        for j in range(9):
            if j == 0:
                Pool.contents[9] = Pool.contents[0]
            else:
                Pool.contents[j-1] = Pool.contents[j]
        Pool.contents[8] = Pool.contents[9]
        Pool.contents[6] += Pool.contents[9]

        Pool.history.append(Pool.count())

    @staticmethod
    def count():
        return sum([Pool.contents[k] for k in range(9)])

    @staticmethod
    def reset():
        Pool.contents = {
            k: 0 for k in range(9)
        }

        Pool.history = []

def construct(input_str):
    # Construct the pool
    numlist = [int(x) for x in input_str.split(',')]
    for num in numlist:
        if num in Pool.contents.keys():
            Pool.contents[num] += 1 
        else:
            Pool.contents[num] = 1

def evolve(days):
    for d in range(days):
        Pool.day()

    # pprint(Pool.contents)
    return Pool.count()

@timeit("Day 06 Part 1")
def part1(input_str, use_rust=False):
    Pool.reset()
    construct(input_str)
    return evolve(80)

@timeit("Day 06 Part 2")
def part2(input_str, use_rust=False):
    Pool.reset()
    construct(input_str)
    return evolve(256)

def test_part1():
    construct('3,4,3,1,2')
    assert Pool.contents == {0: 0, 1: 1, 2: 1, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0}
    evolve(1)
    assert Pool.contents == {0: 1, 1: 1, 2: 2, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    evolve(1)
    assert Pool.contents == {0: 1, 1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 1, 9: 1}

    Pool.reset()
    construct('3,4,3,1,2')
    assert evolve(18) == 26

    Pool.reset()
    assert part1('3,4,3,1,2') == 5934


def test_part2():
    assert part2('3,4,3,1,2') == 26984457539

def plot(input_str):
    Pool.reset()
    construct(input_str)
    evolve(256)

    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(Pool.history)
    ax1.set_xlabel('Day')
    ax1.set_ylabel('# of Lanternfish')
    ax1.grid(True)

    ax2.plot(Pool.history)
    ax2.set_xlabel('Day')
    ax2.set_ylabel('# of Lanternfish')
    ax2.set_yscale('log')
    ax2.grid(True)

    plt.show()
