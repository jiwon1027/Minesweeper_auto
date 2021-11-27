
class BoardIndexOutOfRangeError(Exception):
    pass


import random


def collectAll(board, size, to_find=-1):
    collect = []
    for (i, j) in [(i, j) for i in range(size) for j in range(size)]:
        if board[i][j] == to_find:
            collect.append((i, j))
    return collect


class Board():
    size = 18
    num_mine = 40
    board = []

    def __init__(self, size=18, num_mine=40, random_gen=False):
        if random_gen:
            mine_loc = [(random.randint(0, size - 1), random.randint(0, size - 1)) for i in range(num_mine)]
        else:
            mine_loc = [(6, 0), (15, 9), (17, 6), (5, 12), (1, 16), (5, 3), (14, 0), (1, 2), (2, 3), (1, 11), (1, 11),
                        (14, 12), (3, 7), (12, 1), (1, 16), (15, 8), (7, 16), (16, 17), (6, 1), (13, 12), (8, 7),
                        (8, 9), (2, 7),
                        (0, 3), (12, 16), (3, 5), (15, 4), (17, 7), (5, 10), (14, 10), (15, 16), (15, 13), (4, 2),
                        (14, 15), (4, 12),
                        (2, 14), (6, 9), (10, 15), (14, 16), (8, 12), (8, 4), (3, 8)]

        self.board = [[None for row in range(size)] for col in range(size)]

        for (s, t) in mine_loc:
            self.board[s][t] = -1

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    continue
                count = 0
                for s in range(max(i - 1, 0), min(i + 2, self.size)):
                    for t in range(max(j - 1, 0), min(j + 2, self.size)):
                        if s == i and t == j:
                            continue
                        if self.board[s][t] == -1:
                            count += 1
                self.board[i][j] = count

    def reveal(self, s, t):
        if s < 0 or s >= self.size or t < 0 or t >= self.size:
            print("The reveal index is out of range")
            raise BoardIndexOutOfRangeError

        r = self.board[s][t]

        if r == -1:
            print("You've just revealed a mine.")
            exit()

        return r

    def evaluate(self, play_board):
        if len(play_board) != self.size:
            print("Inappropriate board size")
            return
        this = set(collectAll(self.board, self.size))
        that = set(collectAll(play_board, self.size))

        print("Correct Mines: {}".format(len(this & that)))
        print("InCorrect Mines: {}".format(len(that - this)))
        print("Total Reveals: {}".format(324 - len(collectAll(play_board, self.size, None))))

        pass

    def __repr__(self):
        s = list(map(lambda x: list(map(lambda y: f'{y} ' if y != -1 else '* ', x)), self.board))
        return "\n".join("".join(s[i]) for i in range(self.size))


gameBoard = Board(18, 40)

size = 18
play_board = [ [None for row in range(size)]  for col in range(size)]

def collectWindow(i, j, to_find = -1):
    """
    (i, j) 격자 (Cell) 주변의 to_find 값을 가지는 격자를 모읍니다.
    """
    collect = []
    for s in range(max(i-1, 0), min(i+2, size)):
        for t in range(max(j-1, 0), min(j+2, size)):
            if i == s and j == t:
                continue
            if play_board[s][t] == to_find:
                collect.append((s,t))
    return collect

def printBoard(size):
    s = list(map(lambda x : list(map(lambda y: '* ' if y == -1 else '? ' if y == None else '  ' if y == 0 else f'{y} ', x)), play_board))
    print("\n".join("".join(s[i]) for i in range(size)))
    print("-------------------------------------\n")
    return

def reveal(s, t):
    """
    (s,t)위치의 격자를 엽니다. (open)
    지뢰가 없다면, 주변의 지뢰 갯수를 구할 수 있습니다.
    만약 지뢰가 있었다면, 게임이 종료됩니다. (Game Over)
    """
    v = gameBoard.reveal(s, t)
    play_board[s][t] = v
    #print('{}, {} revealed'.format(s, t))
    #print(v)
    return v

def mark(s, t):
    """
    (s, t) 위치의 격자에 지뢰가 있을 것이라고 표시합니다.
    """
    play_board[s][t] = -1
    #print('{}, {} marked'.format(s, t))
    return

def reveal_zeros(i, j):
    """
    (i, j) 위치의 격자를 밝히고 그 격자 주변에 지뢰가 없다는 것이 밝혀지면,
    그 위치부터 시작하여, 최대한 넓게 격자들을 밝혀냅니다.
    더 좋게 개선할 수 있는 코드입니다.
    """

    if i < 0 or j < 0 or i >= size or j >= size:
        return

    v = reveal(i, j)
    if v != 0:
        return

    for s in range(max(0, i-1), min(size, i+2)):
        for t in range(max(0, j-1), min(size, j+2)):
            if s == i and t == j:
                continue
            if play_board[s][t] != None:
                continue
            v = reveal(s, t)
            if v == 0:
                reveal_zeros(s, t)



def auto_reveal_1(base=1):
    count = 0  # Change count reveal or mark

    for (i, j) in [(i, j) for i in range(size) for j in range(size)]:
        if play_board[i][j] != base:
            continue
        mines = collectWindow(i, j, -1)  # 먼저 주변에 밝혀진 지뢰찾기
        num = len(mines)
        if num == base:
            unknowns = collectWindow(i, j, None)
            for (s, t) in unknowns:
                count += 1
                v = reveal(s, t)
                while auto_reveal_1(v) > 0:
                    continue
                if v == 0:
                    reveal_zeros(s, t)


        elif num > base:
            print("Something Wrong")
            return 0
        elif num < base:
            unknowns = collectWindow(i, j, None)
            if len(unknowns) + num == base:
                for (s, t) in unknowns:
                    mark(s, t)
                    count += 1
    return count


def run():

    if reveal(11, 10) == 0:
        reveal_zeros(11, 10)

    printBoard(18)

    auto_reveal_1(1)


    #print(gameBoard)


run()
gameBoard.evaluate(play_board)