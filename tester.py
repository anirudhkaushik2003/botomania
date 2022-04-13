from player1 import solution as p1
from player2 import solution as p2
import copy
from time import sleep
from prettyprinter import pprint

"""
Everythings (coloumn, row), this was the dumbest decision possible
it fucked with my head so much jesus christ
"""

game_speed = 0.5 # time between moves in seconds, make smaller for faster games

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def valid_pos(x, y):
    return x >= 0 and x <= 14 and y >= 0 and y <= 14

def opponent(x):
    return 1 if x == 2 else 2

class Game:
    active = str
    hill = (int, int)
    board = [[]] # 1 belongs to p1 and 2 belongs to 2
    p1, p2 = None, None
    s1, s2 = int, int

    def __init__(self, ihp, p1, p2):
        self.hill = ihp
        self.active = 1
        self.s1, self.s2 = 0, 0
        self.board = [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2]
        ]
        self.p1 = p1
        self.p2 = p2

    def get_state(self):
        bc = copy.deepcopy(self.board)
        """
            Uncomment the pprint(bc) if you would like your bots perspective
        """
        if self.active == 1:
            for x in range(15):
                for y in range(15):
                    # if manhattan > 3 for all then we cant see it
                    uwu = False
                    for c in range(15):
                        for r in range(15):
                            if bc[c][r] == 1:
                                if manhattan(r, c, x, y) <= 3:
                                    uwu = True
                                    break
                        if uwu:
                            break
                    if not uwu:
                        bc[y][x] = -1
            """Uncomment here for bots perspective"""
            # pprint(bc)
            return {
                'hill': self.hill,
                'board': bc
            }
        else:
            bc = copy.deepcopy(self.board)
            for x in range(15):
                for y in range(15):
                    if self.board[y][x] == 1:
                        bc[y][x] = 2
                    elif self.board[y][x] == 2:
                        bc[y][x] = 1

            # print("whatatatat")
            # pprint(bc)
            for x in range(15):
                for y in range(15):
                    # if manhattan > 3 for all then we cant see it
                    uwu = False
                    for c in range(15):
                        for r in range(15):
                            if bc[c][r] == 1:
                                if manhattan(r, c, x, y) <= 3:
                                    uwu = True
                                    break
                        if uwu:
                            break
                    if not uwu:
                        bc[y][x] = -1
            """Uncomment here for bots perspective"""
            # pprint(bc)
            return {
                'hill': self.hill,
                'board': bc
            }

    def make_move(self):
        if self.active == 1:
            move = p1(self.get_state())
            print("Player 1s Move", move)
        else:
            move = p2(self.get_state())
            print("Player 2s Move", move)
        
        if len(move) == 0:
            None # always legal
        elif len(move) == 5:
            x1, y1, _, x2, y2 = move
            if not valid_pos(x2, y2):
                return 1
            elif not self.board[y1][x1] == self.active:
                return 1
            elif not manhattan(x1, y1, x2, y2) == 1:
                return 1
            elif not self.board[y2][x2] == 0:
                return 1
            self.board[y2][x2] = self.active
            self.board[y1][x1] = 0
        elif len(move) == 3:
            _, x, y = move
            if not valid_pos(x, y):
                return 1
            elif not self.board[y][x] == opponent(self.active):
                return 1
            else:
                # check all players, if none are manhattan == 1, then impossible
                uwu = False
                for r in range(15):
                    for c in range(15):
                        if self.board[r][c] == self.active:
                            if manhattan(c, r, x, y) == 1:
                                uwu = True
                                break
                    if uwu:
                        break
                if uwu == False:
                    return 1
            self.board[y][x] = 0

        # we reached here so it must be a valid move,
        # change active player and update scores
        if self.board[self.hill[1]][self.hill[0]] == 1:
            self.s1 += 1
        elif self.board[self.hill[1]][self.hill[0]] == 2:
            self.s2 += 1
        self.active = opponent(self.active)
        return 0

    def is_game_over(self):
        cnt = {0: 0, 1: 0, 2: 0}
        for x in range(15):
            for y in range(15):
                cnt[self.board[y][x]] += 1
        if cnt[1] == 0 or cnt[2] == 0:
            return True
        return False

def play(g: Game):
    moves = 0
    finished = False
    while g.make_move() != 1:
        print("Hill", g.hill)
        pprint(g.board)
        # this means the bots are making valid moves
        print("Moves", moves)
        moves += 1
        sleep(game_speed)
        g.hill = ((g.hill[0] + 1) % 15, (g.hill[1] - 1) % 15)
        if moves >= 400 or g.is_game_over():
            finished = True
            break
        print()
        print()

    if finished:
        print(f"Scores, p1={g.s1}, p2={g.s2}")
        print(f"Winner - {'Player 1' if g.s1 > g.s2 else 'Player 2'}")
    else:
        print("Invalid Move")

"""
from what ive noticed, the starting hill position is actually not random?
if you did want to make it random, change the tuple to random ints that
lie on the anti diagonal
"""
play(Game((0, 14), p1, p2))