from orrinjelo.utils.decorators import timeit
import numpy as np

VERBOSE=False

def parse_input(input_str):
    draws = [int(x) for x in input_str[0].strip().split(',')]
    nboards = (len(input_str) - 1) // 6
    boards = []
    for i in range(nboards):
        board = []
        for j in range(5):
            line = input_str[2+i*6+j]
            parsed_line = [int(x) for x in line.strip().split()]
            board.append(parsed_line)
        boards.append((np.array(board, dtype=np.int32), np.zeros((5, 5), dtype=np.int32)))

    return draws, boards

def play_round(draws, boards):
    draw = draws.pop(0)
    for b in range(len(boards)):
        boards[b][1][np.where(boards[b][0] == draw)] = 1
    return draw

def is_winner(board):
    board_truth = board[1]
    if np.sum(board_truth) < 5:
        if VERBOSE: print('Failed round num test.')
        return False, None
    for i in range(5):
        if np.sum(board_truth[i,:]) == 5:
            if VERBOSE: print('Succeeded on row.')
            return True, board[0][i,:]
        elif np.sum(board_truth[:,i]) == 5:
            if VERBOSE: print('Succeeded on col.')
            return True, board[0][:,i]
    # if board_truth[0,0] + board_truth[1,1] +  board_truth[2,2] +\
    #   board_truth[3,3] + board_truth[4,4] == 5:
    #     if VERBOSE: print('Succeeded on diag.')
    #     return True, [board[0][j,j] for j in range(5)]
    # elif board_truth[4,0] + board_truth[3,1] +  board_truth[2,2] +\
    #   board_truth[1,3] + board_truth[0,4] == 5:
    #     if VERBOSE: print('Succeeded on quer.')
    #     return True, [board[0][4-j,j] for j in range(5)]
    if VERBOSE: print('Failed.')
    return False, None

def has_winner(boards):
    for board in boards:
        b, _ = is_winner(board)
        if b:
            return True, board
    return False, None

def score(board):
    return np.sum(board[0][board[1]==0])

@timeit("Day 04 Part 1")
def part1(input_str, use_rust=False):
    draws, boards = parse_input(input_str)
    win = False
    while not win:
        draw = play_round(draws, boards)
        win, board = has_winner(boards)
    # print(draw, board)
    return draw * score(board)

@timeit("Day 04 Part 2")
def part2(input_str, use_rust=False):
    draws, boards = parse_input(input_str)
    win = False
    while not win:
        draw = play_round(draws, boards)
        # _, board = has_winner(boards)
        wins = [is_winner(board)[0] for board in boards]
        if sum(wins) == len(boards) - 1:
            loser = wins.index(False)
            while not win:
                draw = play_round(draws, boards)
                win, _ = is_winner(boards[loser])
    return draw * score(boards[loser])


# == Tests ================================

test_input = [
    '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
    '',
    '22 13 17 11  0',
    ' 8  2 23  4 24',
    '21  9 14 16  7',
    ' 6 10  3 18  5',
    ' 1 12 20 15 19',
    '',
    ' 3 15  0  2 22',
    ' 9 18 13 17  5',
    '19  8  7 25 23',
    '20 11 10 24  4',
    '14 21 16 12  6',
    '',
    '14 21 17 24  4',
    '10 16 15  9 19',
    '18  8 23 26 20',
    '22 11 13  6  5',
    ' 2  0 12  3  7',
]

def test_part1():
    draws, boards = parse_input(test_input)

    assert draws == [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1]
    assert len(boards) == 3

    # Try a few fields
    assert boards[0][0][0,4] == 0
    assert boards[1][0][0,2] == 0
    assert boards[2][0][4,1] == 0

    assert np.all(boards[0][1] == 0)

    draw = play_round(draws, boards)

    assert draws == [4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1]
    assert boards[0][1][2,4] == 1
    assert boards[1][1][2,2] == 1
    assert boards[2][1][4,4] == 1
    assert draw == 7

    for _ in range(11):
        draw = play_round(draws, boards)


    assert np.sum(boards[2][1][0,:]) == 5

    assert is_winner(boards[0]) == (False, None)
    assert is_winner(boards[1]) == (False, None)
    assert is_winner(boards[2])[0] == True

    assert has_winner(boards)[0]
    assert score(boards[2]) == 188
    assert score(has_winner(boards)[1]) == 188

    assert part1(test_input) == 4512

def test_part2():
    assert part2(test_input) == 1924

def plot(input_str):
    nboards = (len(input_str) - 1) // 6
    dim = int(nboards**0.5)
    draws, boards = parse_input(input_str)

    import matplotlib.pyplot as plt
    from matplotlib import animation
    import numpy as np

    fig, ax = plt.subplots(figsize=(12, 10))
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])

    plt.grid(True, 'both', color='k')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xticks(list(range(10)))
    plt.yticks(list(range(10)))

    for i in range(dim):
        for j in range(dim):
            board = boards[dim*i + j]
            shape = board[0].shape
            for row in range(shape[0]):
                for col in range(shape[1]):
                    plt.text(row/5 + i, col/5 + j, str(board[0][row, col]))

    def animate(i):
        if len(draws) == 0:
            return
        draw = play_round(draws, boards)
        for b in range(len(boards)):
            x, y = np.where(boards[b][0] == draw)
            if x.shape[0] == 0:
                continue
            # print(b, x[i]/5, (b % 10), y[i]/5, (b//10))
            # # input()
            for i in range(len(x)):
                plt.text(x[i]/5 + (b//10), y[i]/5 + (b % 10), str(draw), color='r')

    anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=len(draws),
                                 interval=100)
    anim.save('day04.gif',writer=animation.FFMpegWriter(fps=10))

    plt.show()

def plot2(input_str):
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    font = pygame.font.SysFont('impact', 18)

    nboards = (len(input_str) - 1) // 6
    dim = int(nboards**0.5)
    draws, boards = parse_input(input_str)

    for i in range(dim):
        for j in range(dim):
            board = boards[dim*i + j]
            shape = board[0].shape
            for row in range(shape[0]):
                for col in range(shape[1]):
                    # plt.text(row/5 + i, col/5 + j, str(board[0][row, col]))
                    text = font.render(str(board[0][row, col]), True, (0,255,0))
                    screen.blit(text, (row*200 + i*20, col*200 + j*20))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
        # screen.fill((255, 255, 255)) 
        # screen.blit(text, (0,0))
        pygame.display.flip() 