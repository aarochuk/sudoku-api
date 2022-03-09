from random import choice, randint
from copy import deepcopy


def find_next(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return y, x

    return None


def valid(board, n, y, x):
    for i in range(9):
        if board[y][i] == n:
            return False

    for i in range(9):
        if board[i][x] == n:
            return False

    x_ = (x//3) * 3
    y_ = (y//3) * 3

    for i in range(3):
        for j in range(3):
            if board[y_ + i][x_ + j] == n:
                return False

    return True


def _solve(board):
    find = find_next(board)
    if find:
        col, row = find
    else:
        return True

    for i in range(1, 10):
        if valid(board, i, col, row):

            board[col][row] = i

            if _solve(board):
                return True

            board[col][row] = 0

    return False


def generate_board(diff=1):
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    poss_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        num = choice(poss_nums)
        board[randint(0, 8)][randint(0, 8)] = num
        poss_nums.remove(num)

    _solve(board)

    empty_board = deepcopy(board)
    if diff == 1:
        for i in range(9):
            del_num = randint(2, 5)
            removed = []
            for j in range(del_num + 1):
                remove = randint(0, 8)
                while remove in removed:
                    remove = randint(0, 8)
                empty_board[i][remove] = 0
                removed.append(remove)

    elif diff == 2:
        for i in range(9):
            del_num = randint(3, 6)
            removed = []
            for j in range(del_num + 1):
                remove = randint(0, 8)
                while remove in removed:
                    remove = randint(0, 8)
                empty_board[i][remove] = 0
                removed.append(remove)

    else:
        amount_1s = 0
        for i in range(9):
            if amount_1s < 2:
                del_num = randint(5, 7)
                if del_num == 7:
                    amount_1s += 1
            else:
                del_num = randint(5, 6)

            removed = []
            for j in range(del_num + 1):
                remove = randint(0, 8)
                while remove in removed:
                    remove = randint(0, 8)
                empty_board[i][remove] = 0
                removed.append(remove)

    return empty_board, board


def string_board(board):
    display = ''
    for i in board:
        for j in i:
            display += str(j) if j != 0 else '.'
    return display


def list_board(board):
    grid = [[], [], [], [], [], [], [], [], []]
    for i in range(len(board)):
        if board[i].isdigit():
            grid[i // 9].append(int(board[i]))
        else:
            grid[i // 9].append(0)

    return grid




