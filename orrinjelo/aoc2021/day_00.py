from orrinjelo.utils.decorators import timeit

@timeit("Day 00 Part 1")
def part1(input_str):
    return 1984

@timeit("Day 00 Part 1")
def part2(input_str):
    return 2077

def test_part1():
    assert part1('George Orwell') == 1984

def test_part2():
    assert part2('Choomba') == 2077