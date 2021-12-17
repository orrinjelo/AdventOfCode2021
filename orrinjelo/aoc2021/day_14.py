from orrinjelo.utils.decorators import timeit
import numpy as np
import sys

history = []

def parse_lines(instr):
    start = instr[0]

    d = {}
    for line in instr[2:]:
        combo, product = line.strip().split('->')
        d[combo.strip()] = product.strip()

    return start, d

def polymerize(chem, d):
    s = ''
    for i in range(len(chem)-1):
        combo = chem[i:i+2]
        insert = d.get(combo, '')
        s += combo[0] + insert
    s += chem[-1]
    return s

def polymerize_n(chem, d, n):
    for i in range(n):
        chem = polymerize(chem, d)
    return chem

def polymerizex(chemd, d, counts):
    cd = chemd.copy()
    for k in cd.keys():
        if cd[k] == 0:
            continue
        insert = d.get(k, None)
        multiplier = cd.get(k)
        if insert in counts.keys():
            counts[insert] += multiplier
        else:
            counts[insert] = multiplier

        one, two = k[0]+insert, insert+k[1]
        chemd[k] -= 1
        if one in chemd.keys():
            chemd[one] += multiplier
        else:
            chemd[one] = multiplier
        if two in chemd.keys():
            chemd[two] += multiplier
        else:
            chemd[two] = multiplier

    return chemd, counts

def polymerizex_n(chem, d, n):
    counts = {}

    chemd = {}
    for i in range(len(chem)-1):
        if chem[i:i+2] in chemd.keys():
            chemd[chem[i:i+2]] += 1
        else:
            chemd[chem[i:i+2]] = 1

    for c in chem:
        if c in counts.keys():
            counts[c] += 1
        else:
            counts[c] = 1
    for i in range(n):
        chemd, counts = polymerizex(chemd, d, counts)
    return chemd, counts

@timeit("Day 14 Part 1")
def part1(input_str, use_rust=False):
    chem, d = parse_lines(input_str)

    # res = polymerize_n(chem, d, 10)
    # counts = [res.count(c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    # print(counts)
    # print(chem)
    # counts.sort()
    # while 0 in counts:
    #     counts.remove(0)

    res, counts = polymerizex_n(chem, d, 3)

    print(counts)
    print(res)


    return max(counts.values()) - min(counts.values())


@timeit("Day 14 Part 2")
def part2(input_str, use_rust=False):
    chem, d = parse_lines(input_str)




# = Test ================================================

inputlist1 = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]

def test_part1():
    chem, d = parse_lines(inputlist1)
    assert chem == 'NNCB'
    assert polymerize(chem, d) == 'NCNBCHB'
    assert len(polymerize_n(chem, d, 5)) == 97

    res = polymerize_n(chem, d, 10)
    # After step 10, B occurs 1749 times, 
    #  C occurs 298 times, H occurs 161 times, and N occurs 865 times
    assert res.count('B') == 1749
    assert res.count('H') == 161

    assert part1(inputlist1) == 1588

def test_part2():
    pass

import pygame
import sys
from pygame import gfxdraw


def plot(input_str):
    pass