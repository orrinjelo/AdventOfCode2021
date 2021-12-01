from orrinjelo.utils.decorators import timeit
from orrinjelo.utils.ops import to_int_list

@timeit("Day 01 Part 1")
def part1(sweeps):
    last = None
    count = 0
    for x in to_int_list(sweeps):
        if last and last < x: # Increased
            count += 1
        last = x
    return count

@timeit("Day 01 Part 2")
def part2(sweeps):
    last = None
    count = 0
    sweeps = to_int_list(sweeps)
    for i in range(0,len(sweeps)-2):
        if last and last < sum(sweeps[i:i+3]): # Increased
            count += 1
        last = sum(sweeps[i:i+3])
    return count

def test_part1():
    sweeps = [
        '199',
        '200',
        '208',
        '210',
        '200',
        '207',
        '240',
        '269',
        '260',
        '263',
    ]
    assert part1(sweeps) == 7

def test_part2():
    sweeps = [
        '199',
        '200',
        '208',
        '210',
        '200',
        '207',
        '240',
        '269',
        '260',
        '263',
    ]    
    assert part2(sweeps) == 5

def plot(sweeps):
    sweeps = to_int_list(sweeps)

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.title('Seafloor Depth')
    plt.plot(sweeps, color='blue', label='raw sonar data')
    plt.plot(range(2, len(sweeps)), [sum(sweeps[i:i+3])/3 for i in range(len(sweeps)-2)], color='red', label='window-smoothed sonar data')
    plt.plot([0 for _ in range(len(sweeps))], 'k--', label='sea level')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.xlabel('Distance from initial drop point (arb.)')
    plt.ylabel('Distance below sea level (arb.)')
    plt.show()
