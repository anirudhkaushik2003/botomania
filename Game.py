import numpy as np
from random import randint
from pdb import set_trace
from Submissions.s011_geodesic import solution as solution2
from Submissions.s010_anchors import solution as solution1

boardStates = {'empty' : 0, 'troop1': 1, 'troop2':2, 'hill' : 4, 'troop1hill': 5, 'troop2hill': 6}
board = np.zeros((15,15), int)
hill = [0,0]
state = {'board' : board, 'hill': hill}
score1 = 0
score2 = 0
move = 0

def illegalMove(move_, troop):
	print('Illegal move by Troop ', troop, ': ' , move_)
	quit()
	
def isFriend(x, y, troop):
	if board[x][y]==troop or board[x][y]==troop+4:
		return True
	return False
	
def getEnemy(troop):
	if troop == 1:
		return 2
	return 1
	
def isEnemy(x,y, troop):
	enemy = getEnemy(troop)
	if board[x][y]==enemy or board[x][y]==enemy+4:
		return True
	return False
	
def distance(x1, y1, x2, y2):
	return abs(x2-x1) + abs(y2-y1)

def drawState():
	global board;
	b = board.copy()
	x = hill[0]
	y = hill[1]
	if b[x][y] == boardStates['empty']:
		b[x][y] = boardStates['hill']
	elif b[x][y] == boardStates['troop1']:
		b[x][y] = boardStates['troop1hill']
	elif b[x][y] == boardStates['troop2']:
		b[x][y] = boardStates['troop2hill']
	else:
		error('Error in drawGame: unknown board square value')
		
	print('   ', end='')
	for ii in range(15):
		print('%2d '%ii, end='')
	print('')
	
	for ii in range(15):
		print('%2d '%ii, end='')
		for jj in range(15):
			if b[ii][jj] == 0:
				if ii==14-jj:
					print('%2s '%'o', end='')
				else:
					print('%2s '%'.', end ='')
			else:
				print('%2d '%b[ii][jj], end = '')
		print('%2d '%ii)
	print('   ', end='')
	for ii in range(15):
		print('%2d '%ii, end='')
	print('')
	print('Move: ', move, ', Troop 1 score: ', score1, ',  Troop 2 score: ', score2)
	

	
def nuke(x,y,troop):
	global board
	if isEnemy(x,y, troop):
		# check if friend is close by
		flag = False
		if x>0 and isFriend(x-1, y, troop):
			flag = True
		elif x<14 and isFriend(x+1, y, troop):
			flag = True
		elif y>0 and isFriend(x, y-1, troop):
			flag = True
		elif y<14 and isFriend(x, y+1, troop):
			flag = True
		if flag == True:
			board[x][y]  -=getEnemy(troop)
			
def walk(x1, y1, x2, y2, troop):
	global board
	global boardStates
	if x2<0 or x2>14 or y2<0 or y2>14:
		illegalMove((y1, x1, 'walk', y2, x2), troop)
	if isFriend(x1, y1, troop):
		if board[x2][y2]==boardStates['empty']:
			if distance(x1, y1, x2, y2) ==1:
				board[x1][y1] = boardStates['empty']
				board[x2][y2] = troop
			else:
				illegalMove((y1, x1, 'walk', y2, x2), troop)
		else:
			illegalMove((y1, x1, 'walk', y2, x2), troop)
				
def prepareBoard(troop):
	global board;
	global boardStates;
	
	def enemy():
		if troop==1:
			return 2
		return 1
	
	b = board.copy();
	for ii in range(15):
		for jj in range(15):
			flag = False;
			for kk in range(max(0, ii-3), min(15, ii+3) ):
				for ll in range(max(0, jj-3), min(15, jj+3 )):
					if isFriend(kk, ll, troop):
						flag = True;
						break
				if flag==True:
					break
			if flag==False:
				b[ii][jj] = -1
			elif board[ii][jj]==enemy():
				b[ii][jj] = 2
			elif board[ii][jj]==troop:
				b[ii][jj]=1
	return b
					
	
	
def nextState():
	global move;
	global board;
	global boardStates;
	global hill;
	global score1
	global score2
	move+=1
	
	# move hill
	hill[0] = hill[0]-1
	if hill[0]<0:
		hill[0] = 14
	hill[1] = 14 - hill[0]
	
	# move troop1
	board1 = prepareBoard(1)
	move_ = solution1({'board' : board1, 'hill' : hill})
	if len(move_) == 0:
		pass; # no move
	elif len(move_)==3:
		if move_[0]=='nuke': # nuke move
			nuke(move_[2], move_[1], 1)
		else:
			illegalMove(move_, 1)
	elif len(move_) == 5:
		if move_[2] == 'walk': # walk move
			walk(move_[1], move_[0], move_[4], move_[3], 1)
		else:
			illegalMove(move_, 1)
	else:
		illegalMove(move_, 1)
	
	# move troop2
	board2 = prepareBoard(2)
	move_ = solution2({'board':board2, 'hill':hill})
	if len(move_) == 0:
		pass; # no move
	elif len(move_)==3:
		if move_[0]=='nuke': # nuke move
			nuke(move_[2], move_[1], 2)
		else:
			illegalMove(move_, 2)
	elif len(move_) == 5:
		if move_[2] == 'walk': # walk move
			walk(move_[1], move_[0], move_[4], move_[3], 2)
		else:
			illegalMove(move_, 2)
	else:
		illegalMove(move_, 2)
	
	# score
	if board[hill[0]][hill[1]] == 1:
		score1 +=1
	if board[hill[0]][hill[1]] == 2:
		score2 +=1
	

	
def startState():
	global board;
	global boardStates;
	global hill;
	
	# set up troop1
	for ii in range(4):
		for jj in range(4-ii):
			board[ii][jj] = boardStates['troop1']
	
	# set up troop2
	for ii in range(11,15):
		for jj in range(14-ii+11, 15):
			board[ii][jj] = boardStates['troop2']
	
	# set up hill
	hillpos = randint(0,14)
	hill = [hillpos, 14-hillpos]
	print(hill)
	
	
if __name__=="__main__":
	startState()
	for ii in range(400):
		drawState()
		input('')
		nextState()
		
		