import random
from time import monotonic as clock
import sys 
sys.setrecursionlimit (500000)

RPLT = 100      # reward per living troop
HR = 500         # hill reward (when my troop on hill)
HP = 50        # hill penalty (when opp troop on hill)

def get_pos(gamestate):
    board = gamestate["board"]
    my_pos = []
    opp_pos = []
    for y in range(15):
        for x in range(15):
            if board[y][x] == -1: continue
            if board[y][x] == 1:
                my_pos.append((y,x))
            elif board[y][x] == 2:
                opp_pos.append((y,x))
    return my_pos,opp_pos

 
def manhattan_distance(x1,y1,x2,y2):
    return (abs(x1-x2)+abs(y1-y2)) 
def euclidean_distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
turn_count = 1
def board_valuation(game):
    board = game.state["board"]
    hill = game.state["hill"]
    valuation = 0
    my_pos,opp_pos = get_pos(game.state)
    diags = [(0,14),(1,13),(2,12),(3,11),(4,10),(5,9),(6,8),(7,7),(8,6),(9,5),(10,4),(11,3),(12,2),(13,1),(14,0)]

    diagPen = [1,1,1,1,1,1,1,2,1,1,1,1,1,1,1]
    # diags2 = []
    # dp2 = []
    # for i in range(len(diags)):
    #     if board[diags[i][1]][diags[i][0]] == 0:
    #         diags2.append(diags[i])
    #         dp2.append(diagPen[i])
    #     elif  board[diags[i][1]][diags[i][0]] == -1:
    #         diags2.append(diags[i])
    #         dp2.append(diagPen[i])
        


    # diags = diags2
    for i in my_pos:
        dist_list = []
        weight_list = []


        for x in range(len(diags)):
            weight_list.append(diagPen[x]*euclidean_distance(diags[x][0],diags[x][1],i[0],i[1])*-1)
            dist_list.append(euclidean_distance(diags[x][0],diags[x][1],i[0],i[1]))

        if len(dist_list):
            dist = min(dist_list)
        else:
            dist = HP
        if dist == 0:
            valuation += HR

        else:
            valuation -= dist

    for i in opp_pos:
        dist_list = []
        weight_list = []

        for x in range(len(diags)):
            weight_list.append(diagPen[x]*euclidean_distance(diags[x][0],diags[x][1],i[0],i[1])*-1)
            dist_list.append(diagPen[x]*euclidean_distance(diags[x][0],diags[x][1],i[0],i[1]))

        if len(dist_list):
            dist = min(dist_list)
            weight = weight_list[dist_list.index(dist)]
        else:
            dist = 0
        if dist == 0:
            valuation -= HP
        else:
            valuation += dist

    return valuation

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def minimaxRoot(depth,valid_moves, game, isMaximisingPlayer):

    board = game.state["board"]
    diags = [(0,14),(1,13),(2,12),(3,11),(4,10),(5,9),(6,8),(7,7),(8,6),(9,5),(10,4),(11,3),(12,2),(13,1),(14,0)]

    diagPen = [1,1,1,1,1,1,1,2,1,1,1,1,1,1,1]
    # diags2 = []
    # dp2 = []
    # for i in range(len(diags)):
    #     if board[diags[i][1]][diags[i][0]] == 0:
    #         diags2.append(diags[i])
    #         dp2.append(diagPen[i])
    #     elif  board[diags[i][1]][diags[i][0]] == -1:
    #         diags2.append(diags[i])
    #         dp2.append(diagPen[i])
        


    # diags = diags2
    
    bestMove = -9999
    bestMoveFound = valid_moves[0]

    for i in valid_moves:
        player = 1 # bot will only be called during its own turn
        game.update(i,player)
        value = minimax(depth - 1, game, -10000, 10000, not isMaximisingPlayer,clock(), clock()+1.0)
        game.undo(i,player)
        if diags:
            if len(i) < 5:
                value -= HR
        if value >= bestMove:
            bestMove = value
            bestMoveFound = i
    return bestMoveFound


def minimax(depth,game, alpha, beta, isMaximisingPlayer,start_time, end_time):
    global turn_count
    turn_count += 1
    # print(turn_count)
    bestMove = -9999
    if turn_count >= 2000: 
        return board_valuation(game)
    if isMaximisingPlayer:
        valid_moves = legal_moves(game.state)
        bestMove = -9999
        player = 1
        for i in valid_moves:
            game.update(i,player)
            bestMove = max(bestMove, minimax(depth-1,game,alpha, beta,not isMaximisingPlayer,start_time,end_time))
            game.undo(i,player)
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
    else:
        player = 2
        bestMove = 9999
        game.update((),player)
        bestMove = min(bestMove,minimax(depth-1,game,alpha, beta,not isMaximisingPlayer,start_time,end_time))
        game.undo((),player)
        beta = min(beta, bestMove)
        if beta <= alpha:
            return bestMove
    return bestMove



class Game:
    def __init__(self,state):
        self.state = state
        
    # finds the next state of the board based on player
    # player = 1 means us, player = 2 means opp
    def update(self, move, player):

        opp = 2
        if player == 2:
            opp = 1
        
        hill = self.state["hill"]
        board = self.state["board"]
        if hill[1] == 0:
            hill2 = (0,14)
            hill = hill2
        else:
            hill2 = (hill[0]+1,hill[1]-1)
            hill = hill2

        if player == 1:
            if len(move) == 5:
                x = move[0]
                y = move[1]
                nx = move[3]
                ny = move[4]
                board[y][x] = 0
                board[ny][nx] = player
                lx = 0
                if nx-3 < 0:
                    lx = 0
                else:   
                    lx = nx - 3
                ly = 0
                if ny-3 < 0:
                    ly = 0
                else:   
                    ly = ny - 3
                ux = 0
                if nx+3 > 14:
                    ux = 14
                else:   
                    ux = nx + 3
                uy = 0
                if ny+3 > 14:
                    uy = 14
                else:   
                    uy = ny + 3
                for y in range(ly,uy):
                    for x in range(lx,ux):
                        if board[y][x] == -1:
                            if manhattan_distance(x,y,nx,ny) <= 3:
                                board[y][x] = 0

            elif len(move) != 0 and len(move) !=3:
                print("Error in length of moves tuple")

        self.state = {'hill': hill, 'board': board}

    
    # finds the previous state of the board based on player
    # player = 1 means us, player = 2 means opp
    def undo( self,move, player):

        opp = 2
        if player == 2:
            opp = 1

        hill = self.state["hill"]
        board = self.state["board"]
        if hill[1] == 14:
            hill2 = (14,0)
            hill = hill2
        else:
            hill2 = (hill[0]-1,hill[1]+1)
            hill = hill2
        if player == 1:
            if len(move) == 5:
                nx = move[0]
                ny = move[1]
                x = move[3]
                y = move[4]
                board[y][x] = 0
                board[ny][nx] = player
                lx = 0
                if nx-3 < 0:
                    lx = 0
                else:   
                    lx = nx - 3
                ly = 0
                if ny-3 < 0:
                    ly = 0
                else:   
                    ly = ny - 3
                ux = 0
                if nx+3 > 14:
                    ux = 14
                else:   
                    ux = nx + 3
                uy = 0
                if ny+3 > 14:
                    uy = 14
                else:   
                    uy = ny + 3
                for y in range(ly,uy+1):
                    for x in range(lx,ux+1):
                        if board[y][x] == 0:
                            if manhattan_distance(x,y,nx,ny) > 3:
                                board[y][x] = -1

            elif len(move) != 0 and len(move) !=3:
                print("Error in length of undo moves tuple")

        self.state = {'hill': hill, 'board': board}



dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]



# returns list of all possible moves, list of coordinates for our troops and opp troops
def legal_moves(gamestate):
    hill = gamestate["hill"]
    board = gamestate["board"]

    valid_moves = []

    for y in range(15):
        for x in range(15):
            if board[y][x] == -1: continue
            if board[y][x] == 1:
                for k in range(4):
                    ny, nx = y + dy[k], x + dx[k]
                    if nx >= 0 and nx < 15 and ny >= 0 and ny < 15:
                        if board[ny][nx] == 2:
                            return([("nuke", nx, ny)])

                        if board[ny][nx] == 0:
                            valid_moves.append((x, y, "walk", nx, ny))
    valid_moves.append(())
    return valid_moves
    # if move in valid_moves:
    #     return true 
    # else:
    #     return false

def filter_vars(valid_moves,game):
    my_pos,opp_pos = get_pos(game.state)
    valid_moves2 = []
    for i in range(len(valid_moves)):
        move = valid_moves[i]
        if len(move) == 5:
            nx = move[3]
            ny = move[4]
            cond = False
            for opp in opp_pos:
                ox = opp[1]
                oy = opp[0]
                if manhattan_distance(nx,ny,ox,oy) == 1:
                    cond = True
                    break
            if not cond:
                valid_moves2.append(move)
        else:
            valid_moves2.append(move)
        

    return valid_moves2

# function that finds all valid moves for oppoent based on board, list of opp_pos
def opp_moves(game):
    board = game.state["board"]
    valid_moves = []
    my_pos, opp_pos = get_pos(game.state)
    for i in opp_pos:
        y = i[0]
        x = i[1]
        for k in range(4):
            ny, nx = y + dy[k], x + dx[k]
            if nx >= 0 and nx < 15 and ny >= 0 and ny < 15:
                if board[ny][nx] == 1:
                    return([("nuke", nx, ny)])
                if board[ny][nx] == 0 or board[ny][nx] == -1:
                    valid_moves.append((x, y, "walk", nx, ny)) 

    return valid_moves


def solution(gamestate: dict):
    valid_moves = legal_moves(gamestate)
    game = Game(gamestate)
    valid_moves = filter_vars(valid_moves,game)
    return  minimaxRoot(4,valid_moves,game, True)
    # print( minimaxRoot(4,valid_moves,game, True))

# gamestate = {'board': [[1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1], [1, 1, 1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1], [1, 1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [0, 0, 1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]], 'hill': [4, 10]}
# solution(gamestate)

# gamestate = {'board':
# [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ],
# 'hill': [8, 6]
# }
# print(board_valuation(Game(gamestate)))
