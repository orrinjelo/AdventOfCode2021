from orrinjelo.utils.decorators import timeit
# from orrinjelo.aoc2021.rust.pyaoc import day03_part1, day03_part2

# @timeit("Day 03 Part 1")
def part1(report, use_rust=False):
    if use_rust:
        return 0 #day02_part1(instructions)

    power = len(report[0].strip()) - 1

    gamma, epsilon = 0, 0
    for i in range(len(report[0].strip())):
        ones, zeros = 0, 0
        for line in report:
            if line.strip()[i] == '1':
                ones += 1
            else:
                zeros += 1
        if ones >= zeros:
            gamma += 2**power
        if ones <= zeros:
            epsilon += 2**power
        power -= 1

    return gamma, epsilon, gamma*epsilon

# @timeit("Day 03 Part 2")
def part2(report, use_rust=False):
    if use_rust:
        return 0 # day02_part2(instructions)

    oxygen, co2 = 0, 0
    olist = [x.strip() for x in report]
    clist = [x.strip() for x in report]
    xlist = [x.strip() for x in report]
    for i in range(len(report[0].strip())):
        ones, zeros = 0, 0
        for line in olist:
            if line[i] == '1':
                ones += 1
            else:
                zeros += 1
        if ones >= zeros:
            newolist = [x for x in olist if x[i] == '1']
            if len(olist) != 1: olist = newolist[:]
        elif ones < zeros:
            newolist = [x for x in olist if x[i] == '0']
            if len(olist) != 1: olist = newolist[:]

        ones, zeros = 0, 0
        for line in clist:
            if line[i] == '1':
                ones += 1
            else:
                zeros += 1
        if ones >= zeros:
            newclist = [x for x in clist if x[i] == '0']
            if len(clist) != 1: clist = newclist[:]
        elif ones < zeros:
            newclist = [x for x in clist if x[i] == '1']
            if len(clist) != 1: clist = newclist[:]

        # print(olist, clist)

        if len(olist) == 1 and len(clist) == 1:
            # oxygen = int(olist[0], 2)
            # co2 = int(clist[0], 2)
            break

    oxygen = sum([int(i, 2) for i in olist])
    co2 = sum([int(i, 2) for i in clist])

    return oxygen, co2, oxygen*co2

def test_part1():
    inp = [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010',
    ]
    assert part1(inp) == (22, 9, 198)

def test_part2():
    inp = [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010',
    ]
    assert part2(inp) == (23, 10, 230)

def plot(report):
    import matplotlib.pyplot as plt
    from matplotlib import animation
    import numpy as np

    def barlist(n): 
        gamma, epsilon, _ = part1(report[:n])
        o2, co2, _ = part2(report[:n])
        return [gamma, epsilon*10, o2, co2*10]

    fig, ax = plt.subplots()
    # fig=plt.figure()

    n=len(report) #Number of frames
    x=range(1,5)
    barcollection = plt.bar(x,barlist(1))
    cols = ('', 'gamma', 'epsilon (x10)', 'oxygen', 'co2 (x10)')
    xpos = np.arange(len(cols))
    ax.set_xticks(xpos)
    ax.set_xticklabels(cols)
    ax.set_title('Power and Life Support')
    ax.set_ylim(0,5000)

    def animate(i):
        y=barlist(i+1)
        for i, b in enumerate(barcollection):
            b.set_height(y[i])

    anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n,
                                 interval=100)

    anim.save('day03.gif',writer=animation.FFMpegWriter(fps=10))
    plt.show()
