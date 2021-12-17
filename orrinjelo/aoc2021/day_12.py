from orrinjelo.utils.decorators import timeit
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.setrecursionlimit(5000)

def parse_graph(lines):
    connections = [(y[0],y[1]) for y in [x.strip().split('-') for x in lines]]

    G = nx.Graph()
    for c in connections:
        G.add_edge(c[0], c[1])

    return G

# Returns count of paths from 's' to 'd'
def countPaths(G, s, d):
    nodelist = list(G.nodes)
    npG = nx.to_numpy_array(G, nodelist=nodelist)

    # Mark all the vertices
    # as not visited
    visited = [False] * len(nodelist)

    # Call the recursive helper
    # function to print all paths
    pathCount = [0]
    countPathsRecurse(npG, nodelist, s, d, visited, pathCount)
    return pathCount[0]

def countPathsRecurse(npG, nodelist, u, d,
                   visited, pathCount):
    j = nodelist.index(u)
    if u.islower():
        visited[j] = True

    # If current vertex is same as
    # destination, then increment count
    if u == d:
        pathCount[0] += 1

    # If current vertex is not destination
    else:

        # Recur for all the vertices
        # adjacent to current vertex
        for i in range(len(nodelist)):
            if i == j:
                continue
            if npG[j,i] == 0:
                continue
            if (not visited[i]):
                countPathsRecurse(npG, nodelist, nodelist[i], d,
                                    visited, pathCount)

    visited[j] = False


# Returns count of paths from 's' to 'd'
def countPaths2(G, s, d):
    nodelist = list(G.nodes)
    npG = nx.to_numpy_array(G, nodelist=nodelist)

    print("Nodes:", nodelist)

    # Mark all the vertices
    # as not visited
    visited = [False] * len(nodelist)

    # Call the recursive helper
    # function to print all paths
    pathCount = [0]
    doubley_visited = False
    countPathsRecurse2(npG, nodelist, s, d, visited, pathCount, [])
    return pathCount[0]

def containsTwoLowercase(hist):
    for node in hist:
        if node.islower() and hist.count(node) == 2:
            return True
    return False

def countPathsRecurse2(npG, nodelist, u, d,
                   visited, pathCount, history=[]):
    j = nodelist.index(u)
    if u.islower():
        if visited[j] and containsTwoLowercase(history):
            return
        visited[j] = True

    history.append(u)

    # If current vertex is same as
    # destination, then increment count
    if u == d:
        pathCount[0] += 1


    # If current vertex is not destination
    else:

        # Recur for all the vertices
        # adjacent to current vertex
        for i in range(len(nodelist)):
            if i == j:
                continue
            if npG[j,i] == 0:
                continue
            if nodelist[i] == 'start':
                continue

            if not visited[i] or (visited[i] and not containsTwoLowercase(history)):
                countPathsRecurse2(npG, nodelist, nodelist[i], d,
                                    visited[:], pathCount, history)

    history.pop()
    visited[j] = False


@timeit("Day 12 Part 1")
def part1(input_str, use_rust=False):
    G = parse_graph(input_str)

    return countPaths(G, 'start', 'end')


@timeit("Day 12 Part 2")
def part2(input_str, use_rust=False):
    G = parse_graph(input_str)

    return countPaths2(G, 'start', 'end')



# = Test ================================================

inputlist1 = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]

inputlist2 = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc',
]

inputlist3 = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW',
]

def test_part1():
    assert part1(inputlist1) == 10
    assert part1(inputlist2) == 19
    assert part1(inputlist3) == 226


def test_part2():
    assert part2(inputlist1) == 36
    assert part2(inputlist2) == 103
    assert part2(inputlist3) == 3509

import pygame
import sys


def plot(input_str):
    G = parse_graph(input_str)
    
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")    
    options = {
        "font_size": 12,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 5,
    }
    nx.draw_networkx(G, nx.spring_layout(G), **options)

    plt.show()
