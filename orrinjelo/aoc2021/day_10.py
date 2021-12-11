from orrinjelo.utils.decorators import timeit

points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def parse_line(l):
    stack = []
    errstr = 'Expected {} but found {} instead.'
    for c in l.strip():
        if c in '[({<':
            stack.append(c)
        else:
            x = stack.pop()
            if c == ')':
                if x != '(':
                    print(errstr.format(c, ']' if x == '[' else '}' if x == '{' else '>'))
                    return 3, stack
            elif c == ']':
                if x != '[':
                    print(errstr.format(c, ')' if x == '(' else '}' if x == '{' else '>'))
                    return 57, stack
            elif c == '}':
                if x != '{':
                    print(errstr.format(c, ']' if x == '[' else ')' if x == '(' else '>'))
                    return 1197, stack
            elif c == '>':
                if x != '<':
                    print(errstr.format(c, ']' if x == '[' else ')' if x == '(' else '}'))
                    return 25137, stack
    return 0, stack

def complete_line(stack):
    score = 0
    for c in stack:
        score *= 5
        # print('Score (1):', score)
        score += points[c]
        # print('Score (2):', score)
    return score

@timeit("Day 10 Part 1")
def part1(input_str, use_rust=False):
    return sum(parse_line(line)[0] for line in input_str)

@timeit("Day 09 Part 2")
def part2(input_str, use_rust=False):
    incompletes = []
    for line in input_str:
        points, stack = parse_line(line)
        if points == 0:
            incompletes.append(stack)

    scores = []
    # print(incompletes)
    for stack in incompletes:
        stack.reverse()
        scores.append(complete_line(stack))

    scores.sort()
    # print(scores)
    return scores[len(scores)//2]


# = Test ================================================

inputlist = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]

def test_part1():
    assert part1(inputlist) == 26397


def test_part2():
    assert complete_line('{{[[({([') == 288957
    assert part2(inputlist) == 288957

import pygame
import sys

def draw_pill(surface, pill_type, x, y):
    if pill_type in '{}':
        color = (255,0,0)
    elif pill_type in '[]':
        color = (255,255,0)
    elif pill_type in '()':
        color = (0,0,255)
    elif pill_type in '<>':
        color = (240,0,240)
    else:
        print('Unknown:',pill_type)
        color = (0,0,0)

    pygame.draw.rect(surface, color, pygame.Rect(x*5, y*5, 5, 5))

def plot(input_str):
    entries = []
    for line in input_str:
        points, stack = parse_line(line)
        entries.append((points==0, ''.join([line.strip(),*stack])))

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((640,480))
    surface = pygame.Surface((640,480))

    input()
    frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();

        # erase the screen
        screen.fill((255, 255, 255))

        for e in range(len(entries)):
            try:
                for x in range(frame):
                    draw_pill(screen, entries[e][1][x], x, e)
            except Exception as err:
                print(err, e, len(entries[e][1]), frame)

        pygame.display.update()
        surface.blit(screen, (0,0))

        clock.tick(30)
        frame += 1