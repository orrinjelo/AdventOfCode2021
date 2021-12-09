from orrinjelo.utils.decorators import timeit

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

digits = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}

rdigits = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}

xdigits = {
    0: 'abcdefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

def parse(lines):
    entries = []
    for line in lines:
        parts = line.split('|')
        inputs = parts[0].strip().split()
        outputs = parts[1].strip().split()
        entries.append((inputs, outputs))

    return entries

def parse_digits(inputs, outputs):
    d = {}
    f = {}
    iwords = [''.join(sorted(list(word))) for word in inputs]
    owords = [''.join(sorted(list(word))) for word in outputs]

    # First pass: 1, 7, 4, 8
    for sword in iwords:
        if len(sword) == 2:
            d[sword] = 1
            f[1] = sword
        elif len(sword) == 3:
            d[sword] = 7
            f[7] = sword
        elif len(sword) == 4:
            d[sword] = 4
            f[4] = sword
        elif len(sword) == 7:
            d[sword] = 8
            f[8] = sword
    for k in d.keys():
        iwords.remove(k)


    # Second pass: 3(contains 1), 9 (contains 1, 4, 7), 0 (contains 1, 7)
    for sword in iwords:
        if sword in d.keys():
            continue
        if len(sword) == 5 and f[1][0] in sword and f[1][1] in sword:
            d[sword] = 3
            f[3] = sword
        elif len(sword) == 6 and f[4][0] in sword and f[4][1] in sword and f[4][2] in sword and f[4][3] in sword:
            d[sword] = 9
            f[9] = sword
        elif len(sword) == 6 and f[1][0] in sword and f[1][1] in sword:
            d[sword] = 0
            f[0] = sword
    for k in d.keys():
        if k in iwords: iwords.remove(k)        

    # Third pass: 5 (is contained in 9)
    for sword in iwords:
        if len(sword) == 5 and sword[0] in f[9] and sword[1] in f[9] and sword[2] in f[9] and sword[3] in f[9] and sword[4] in f[9]:
            d[sword] = 5
            f[5] = sword
        elif len(sword) == 6:
            d[sword] = 6
            f[6] = sword
    for k in d.keys():
        if k in iwords: iwords.remove(k)        

    assert len(iwords) == 1
    # Add 2
    d[iwords[0]] = 2
    f[2] = iwords[0]

    res = []
    # Convert output
    for sword in owords:
        res.append(d[sword])

    return res


@timeit("Day 08 Part 1")
def part1(input_str, use_rust=False):
    # In the output values, how many times do digits 1, 4, 7, or 8 appear?
    entries = parse(input_str)
    count = 0
    for entry in entries:
        for word in entry[1]:
            if len(word) in [2, 3, 4, 7]:
                count += 1

    return count

@timeit("Day 08 Part 2")
def part2(input_str, use_rust=False):
    entries = parse(input_str)
    results = [parse_digits(*x) for x in entries]
    results = [x[0]*1000 + x[1]*100 + x[2]*10 + x[3] for x in results]
    return sum(results)

# = Test ================================================

inputlist = [
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
]


def test_part1():
    assert part1(inputlist) == 26

    # fdgacbe cefdb cefbgd gcbe: 8394
    # fcgedb cgb dgebacf gc: 9781
    # cg cg fdcagb cbg: 1197
    # efabcd cedba gadfec cb: 9361
    # gecf egdcabf bgf bfgea: 4873
    # gebdcfa ecba ca fadegcb: 8418
    # cefg dcbef fcge gbcadfe: 4548
    # ed bcgafe cdgba cbgef: 1625
    # gbdfcae bgc cg cgb: 8717
    # fgae cfgab fg bagce: 4315

def test_part2():
    entries = parse(inputlist)
    assert parse_digits(*entries[0]) == [8,3,9,4]
    assert parse_digits(*entries[1]) == [9,7,8,1]
    assert parse_digits(*entries[2]) == [1,1,9,7]
    assert parse_digits(*entries[3]) == [9,3,6,1]
    assert parse_digits(*entries[4]) == [4,8,7,3]
    assert parse_digits(*entries[5]) == [8,4,1,8]
    assert parse_digits(*entries[6]) == [4,5,4,8]
    assert parse_digits(*entries[7]) == [1,6,2,5]
    assert parse_digits(*entries[8]) == [8,7,1,7]
    assert parse_digits(*entries[9]) == [4,3,1,5]

    assert part2(inputlist) == 61229    

import pygame
import numpy as np

class Digit():
    def __init__(self, screen, x, y, lit=[]):
        self.lit = lit
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self):
        vert = lambda x, y: [
            (0+x, 2 +y),
            (0+x, 18+y),
            (2+x, 20+y),
            (4+x, 18+y),
            (4+x, 2 +y),
            (2+x, 0 +y),
        ]
        horiz = lambda x, y: [
            (2 +x, 0+y),
            (18+x, 0+y),
            (20+x, 2+y),
            (18+x, 4+y),
            (2 +x, 4+y),
            (0 +x, 2+y),
        ]

        # print(self.lit)

        if 'a' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, horiz(self.x*40 + 4, self.y*60 + 0), 1)
        if 'b' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, vert(self.x*40 + 0, self.y*60 + 4), 1)
        if 'c' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, vert(self.x*40 + 24, self.y*60 + 4), 1)
        if 'd' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, horiz(self.x*40 + 4, self.y*60 + 24), 1)
        if 'e' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, vert(self.x*40 + 0, self.y*60 + 28), 1)
        if 'f' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, vert(self.x*40 + 24, self.y*60 + 28), 1)
        if 'g' in self.lit:
            pygame.draw.lines(self.screen, (20, 20, 20), True, horiz(self.x*40 + 4, self.y*60 + 48), 1)

def plot(input_str):
    entries = parse(input_str)
    results = [parse_digits(*x) for x in entries]
    # results = [x[0]*1000 + x[1]*100 + x[2]*10 + x[3] for x in results]

    pygame.init()

    screen = pygame.display.set_mode((640,480))

    digits = [Digit(screen, x, y, lit=list('abcdefg')) for x in range(10) for y in range(8)]
    outputs = [Digit(screen, x+12, y, lit=list('abcdefg')) for x in range(4) for y in range(8)]
    clock = pygame.time.Clock()

    count = 0

    input()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();

        # erase the screen
        screen.fill((255, 255, 255))

        # draw the updated picture

        for d in range(len(digits)):
            digits[d].draw()
            digits[d].lit = set(np.random.choice(list('abcdefg'),5)) if count < 60+d else entries[d//10][0][d%10]

        for d in range(len(outputs)):
            outputs[d].draw()
            outputs[d].lit = set(np.random.choice(list('abcdefg'),5)) if count < 80+d*10+d else list(xdigits[results[d][d%4]]) if count % 20 < 19 else entries[d//4][1][d%4]

        # print(count)

        # update the screen
        pygame.display.update()
        clock.tick(30)
        count += 1