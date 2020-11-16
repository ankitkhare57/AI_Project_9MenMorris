from Utility import *
import copy

def adjacentLocations(position):
	'''
	Return pieces adjacent to the piece at position
	@param position: index of the piece
	'''
	adjacent = [
		[1, 3],
		[0, 2, 9],
		[1, 4],
		[0, 5, 11],
		[2, 7, 12],
		[3, 6],
		[5, 7, 14],
		[4, 6],
		[9, 11],
		[1, 8, 10, 17],
		[9, 12],
		[3, 8, 13, 19],
		[4, 10, 15, 20],
		[11, 14],
		[6, 13, 15, 22],
		[12, 14],
		[17, 19],
		[9, 16, 18],
		[17, 20],
		[11, 16, 21],
		[12, 18, 23],
		[19, 22],
		[21, 23, 14],
		[20, 22]
	]

	adjacent_6 = [
        [1, 3], [0, 2, 9], [1, 4],
        [0, 5, 11], [2, 7, 12],
        [3, 6], [5, 7, 14],
        [4, 6], [9, 11],
        [1, 8, 10], [9, 12],
        [3, 8, 13],
        [4, 10, 15], [11, 14],
        [6, 13, 15], [12, 14]
    ]
	return adjacent_6[position]

def checkMillFormation(position, board, player):
	'''
	Return True if there's a mill at position for player on given board
	@param position: the index of the position we're checking
	@param board: the list of the current board
	@param player: string representation of the board piece color
	'''

	mill = [
		(isMill(player, board, 1, 2) or isMill(player, board, 3, 5)),
		(isMill(player, board, 0, 2) or isMill(player, board, 9, 17)),
		(isMill(player, board, 0, 1) or isMill(player, board, 4, 7)),
		(isMill(player, board, 0, 5) or isMill(player, board, 11, 19)),
		(isMill(player, board, 2, 7) or isMill(player, board, 12, 20)),
		(isMill(player, board, 0, 3) or isMill(player, board, 6, 7)),
		(isMill(player, board, 5, 7) or isMill(player, board, 14, 22)),
		(isMill(player, board, 2, 4) or isMill(player, board, 5, 6)),
		(isMill(player, board, 9, 10) or isMill(player, board, 11, 13)),
		(isMill(player, board, 8, 10) or isMill(player, board, 1, 17)),
		(isMill(player, board, 8, 9) or isMill(player, board, 12, 15)),
		(isMill(player, board, 3, 19) or isMill(player, board, 8, 13)),
		(isMill(player, board, 20, 4) or isMill(player, board, 10, 15)),
		(isMill(player, board, 8, 11) or isMill(player, board, 14, 15)),
		(isMill(player, board, 13, 15) or isMill(player, board, 6, 22)),
		(isMill(player, board, 13, 14) or isMill(player, board, 10, 12)),
		(isMill(player, board, 17, 18) or isMill(player, board, 19, 21)),
		(isMill(player, board, 1, 9) or isMill(player, board, 16, 18)),
		(isMill(player, board, 16, 17) or isMill(player, board, 20, 23)),
		(isMill(player, board, 16, 21) or isMill(player, board, 3, 11)),
		(isMill(player, board, 12, 4) or isMill(player, board, 18, 23)),
		(isMill(player, board, 16, 19) or isMill(player, board, 22, 23)),
		(isMill(player, board, 6, 14) or isMill(player, board, 21, 23)),
		(isMill(player, board, 18, 20) or isMill(player, board, 21, 22)),
	]

	return mill[position]

def isMill(player, board, pos1, pos2):
	'''
	Return True if pos1 and pos2 on board both belong to player
	@param player: string representation of the board piece color
	@param board: current list
	@param pos1: first position index
	@param pos2: second position index
	'''

	if (board[pos1] == player and board[pos2] == player):
		return True
	return False


# Return True if a player has a mill on the given position
# def isMill_BaselineAI(position, board):
#     player = board[position]
#     if player != 'x':
#         return checkMillFormation(position, board, player)
#     else:
#         return False

def isMill_BaselineAI(position, board):
    player = board[position]
    if player != 'x':
        return checkNextMill_six(position, board, player)
    else:
        return False

# def isCloseMill(position, board):
# 	'''
# 	Return True if any player has a mill on position
# 	@param position: the index of the position we're checking
# 	@param board: the list of the current board
# 	'''

# 	player = board[position]

# 	# if position is not empty
# 	if (player != "X"):
# 		return checkMillFormation(position, board, player)
	
# 	return False

def isCloseMill(position, board):
	'''
	Return True if any player has a mill on position
	@param position: the index of the position we're checking
	@param board: the list of the current board
	'''

	player = board[position]

	# if position is not empty
	if (player != "X"):
		return checkNextMill_six(position, board, player)
	
	return False


# Checks whether all pieces owned by the player are Mill
def allIsMill(board, player):
    isMill = False
    for i in range(len(board)):
        if (board[i] == player):
            if checkMillFormation(i, board, player):
                isMill = True
            else:
                return False
    return isMill

def stage1Moves(board):
	'''
	'''
	board_list = []

	for i in range(len(board)):
		# fill empty positions with white
		if (board[i] == "X"):
			board_clone = copy.deepcopy(board)
			board_clone[i] = "1"

			if (isCloseMill(i, board_clone)):
				board_list = removePiece(board_clone, board_list)
			else:
				board_list.append(board_clone)
	return board_list

def stage2Moves(board):
	'''

	@param board: current list
	'''
	board_list = []
	for i in range(len(board)):
		if (board[i] == "1"):
			adjacent_list = adjacentLocations(i)

			for pos in adjacent_list:
				if (board[pos] == "X"):
					board_clone = copy.deepcopy(board)
					board_clone[i] = "X"
					board_clone[pos] = "1"

					if isCloseMill(pos, board_clone):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def stage3Moves(board):
	'''
	'''
	board_list = []

	for i in range(len(board)):
		if (board[i] == "1"):

			for j in range(len(board)):
				if (board[j] == "X"):
					board_clone = copy.deepcopy(board)

					board_clone[i] = "X"
					board_clone[j] = "1"

					if (isCloseMill(j, board_clone)):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def stage23Moves(board):
	if (numOfValue(board, "1") == 3):
		return stage3Moves(board)
	else:
		return stage2Moves(board)

def removePiece(board_clone, board_list):
	'''
	'''
	for i in range(len(board_clone)):
		if (board_clone[i] == "2"):

			if not isCloseMill(i, board_clone):
				new_board = copy.deepcopy(board_clone)
				new_board[i] = "X"
				board_list.append(new_board)
	return board_list

def getPossibleMillCount(board, player):
	'''
	'''
	count = 0

	for i in range(len(board)):
		if (board[i] == "X"):
			# if checkMillFormation(i, board, player):
			if checkNextMill_six(i, board, player):
				count += 1
	return count

def getEvaluationStage23(board):
	'''
	'''
	
	numWhitePieces = numOfValue(board, "1")
	numBlackPieces = numOfValue(board, "2")
	mills = getPossibleMillCount(board, "1")

	evaluation = 0

	board_list = stage23Moves(board)

	numBlackMoves = len(board_list)

	if numBlackPieces <= 2 or numBlackPieces == 0:
		return float('inf')
	elif numWhitePieces <= 2:
		return float('-inf')
	else:
		return 0

def potentialMillInFormation(position, board, player):
	'''
	'''
	adjacent_list = adjacentLocations(position)

	for i in adjacent_list:
		# if (board[i] == player) and (not checkMillFormation(position, board, player)):
		if (board[i] == player) and (not checkNextMill_six(position, board, player)):
			return True
	return False

def getPiecesInPotentialMillFormation(board, player):
	'''
	'''
	count = 0

	for i in range(len(board)):
		if (board[i] == player):
			adjacent_list = adjacentLocations(i)
			for pos in adjacent_list:
				if (player == "1"):
					if (board[pos] == "2"):
						board[i] = "2"
						if isCloseMill(i, board):
							count += 1
						board[i] = player
				else:
					if (board[pos] == "1" and potentialMillInFormation(pos, board, "1")):
						count += 1
	return count

# For board variation
# Printing board
def print_board_six(board):
	print(board[0]+"(00)"+"----------------"+board[1]+"(01)"+"----------------"+board[2]+"(02)")
	#print("|                    |                        |")
	print("|      "+board[8]+"(08)"+"---------"+board[9]+"(09)"+"-------"+board[10]+"(10)"+"        |")
	print(board[3]+"(03)"+"--"+board[11]+"(11)"+"                     "+board[12]+"(12)"+"----"+board[4]+"(04)")
	print("|      "+board[13]+"(13)"+"---------"+board[14]+"(14)"+"-------"+board[15]+"(15)"+"        |")
	#print("|                    |                        |")
	print(board[5]+"(05)"+"----------------"+board[6]+"(06)"+"----------------"+board[7]+"(07)")

def print_board_nine(board):
	print(board[0]+"(00)"+"------------------------"+board[1]+"(01)"+"-----------------------"+board[2]+"(02)")
	#print("|                              |                             |")
	print("|         "+board[8]+"(08)"+"--------------"+board[9]+"(09)"+"------------"+board[10]+"(10)"+"          |")
	print("|         |      "+board[16]+"(16)"+"-------"+board[17]+"(17)"+"-----"+board[18]+"(18)"+"      |          |")
	print(board[3]+"(03)"+"-----"+board[11]+"(11)"+"--"+board[19]+"(19)"+"                 "+board[20]+"(20)"+"--"+board[12]+"(12)"+"-------"+board[4]+"(04)")
	print("|         |      "+board[21]+"(21)"+"-------"+board[22]+"(22)"+"-----"+board[23]+"(23)"+"      |          |")
	print("|         "+board[13]+"(13)"+"--------------"+board[14]+"(14)"+"------------"+board[15]+"(15)"+"          |")
	#print("|                              |                             |")
	print(board[5]+"(05)"+"------------------------"+board[6]+"(06)"+"-----------------------"+board[7]+"(07)")

def print_board_twelve(board):
	print(board[0]+"(00)"+"--------------------------------"+board[1]+"(01)"+"------------------------------"+board[2]+"(02)")
	#print("|                              |                             |")
	print("|          "+board[8]+"(08)"+"---------------------"+board[9]+"(09)"+"-----------------"+board[10]+"(10)"+"            |")
	print("|             |      "+board[16]+"(16)"+"-----------"+board[17]+"(17)"+"----------"+board[18]+"(18)"+"     |             |")
	print("|             |        |     "+board[24]+"(24)"+"---"+board[25]+"(25)"+"---"+board[26]+"(26)"+"    |       |             |")
	print(board[3]+"(03)"+"------"+board[11]+"(11)"+"-----"+board[19]+"(19)"+"---"+board[27]+"(27)"+"           "+board[28]+"(28)"+"---"+board[20]+"(20)"+"--"+board[12]+"(12)"+"--------"+board[4]+"(04)")
	print("|             |        |     "+board[29]+"(29)"+"---"+board[30]+"(30)"+"---"+board[31]+"(31)"+"    |       |             |")
	print("|             |      "+board[21]+"(21)"+"-----------"+board[22]+"(22)"+"----------"+board[23]+"(23)"+"     |             |")
	print("|          "+board[13]+"(13)"+"---------------------"+board[14]+"(14)"+"------------------"+board[15]+"(15)"+"           |")
	print(board[5]+"(05)"+"--------------------------------"+board[6]+"(06)"+"------------------------------"+board[7]+"(07)")

def print_board_fifteen(board):
	print(board[0]+"(00)"+"------------------------------------------------"+board[1]+"(01)"+"------------------------------------------------"+board[2]+"(02)")
	print("|         "+board[8]+"(08)"+"--------------------------------------"+board[9]+"(09)"+"--------------------------------------"+board[10]+"(10)"+"         |")
	print("|         |         "+board[16]+"(16)"+"----------------------------"+board[17]+"(17)"+"----------------------------"+board[18]+"(18)"+"         |         |")
	print("|         |         |      "+board[24]+"(24)"+"---------------------"+board[25]+"(25)"+"---------------------"+board[26]+"(26)"+"      |         |         |")
	print("|         |         |      |         "+board[32]+"(32)"+"-----------"+board[33]+"(33)"+"-----------"+board[34]+"(34)"+"         |      |         |         |")
	print(board[3]+"(03)"+"-----"+board[11]+"(11)"+"-----"+board[19]+"(19)"+"--"+board[27]+"(27)"+"-----"+board[35]+"(35)"+"                           "+board[36]+"(36)"+"-----"+board[28]+"(28)"+"--"+board[20]+"(20)"+"-----"+board[12]+"(12)"+"-----"+board[4]+"(04)")
	print("|         |         |      |         "+board[37]+"(37)"+"-----------"+board[38]+"(38)"+"-----------"+board[39]+"(39)"+"         |      |         |         |")
	print("|         |         |      "+board[29]+"(29)"+"---------------------"+board[30]+"(30)"+"-----------"+"-----------"+board[31]+"(31)"+"     |         |         |")
	print("|         |         "+board[21]+"(21)"+"----------------------------"+board[22]+"(22)"+"----------------------------"+board[23]+"(23)"+"         |         |")
	print("|         "+board[13]+"(13)"+"--------------------------------------"+board[14]+"(14)"+"--------------------------------------"+board[15]+"(15)"+"         |")
	print(board[5]+"(05)"+"------------------------------------------------"+board[6]+"(06)"+"------------------------------------------------"+board[7]+"(07)")

def print_board_eighteen(board):
	print(board[0]+"(00)"+"------------------------------------------------------------"+board[1]+"(01)"+"------------------------------------------------------------"+board[2]+"(02)")
	print("|         "+board[8]+"(08)"+"--------------------------------------------------"+board[9]+"(09)"+"--------------------------------------------------"+board[10]+"(10)"+"         |")
	print("|         |         "+board[16]+"(16)"+"----------------------------------------"+board[17]+"(17)"+"----------------------------------------"+board[18]+"(18)"+"         |         |")
	print("|         |         |      "+board[24]+"(24)"+"---------------------------------"+board[25]+"(25)"+"---------------------------------"+board[26]+"(26)"+"      |         |         |")
	print("|         |         |      |         "+board[32]+"(32)"+"-----------------------"+board[33]+"(33)"+"-----------------------"+board[34]+"(34)"+"         |      |         |         |")
	print("|         |         |      |         |         "+board[40]+"(40)"+"-------------"+board[41]+"(41)"+"-------------"+board[42]+"(42)"+"         |         |      |         |         |")
	print(board[3]+"(03)"+"-----"+board[11]+"(11)"+"-----"+board[19]+"(19)"+"--"+board[27]+"(27)"+"-----"+board[35]+"(35)"+"-----"+board[43]+"(43)"+"                               "+board[44]+"(44)"+"-----"+board[36]+"(36)"+"-----"+board[28]+"(28)"+"--"+board[20]+"(20)"+"-----"+board[12]+"(12)"+"-----"+board[4]+"(04)")
	print("|         |         |      |         |         "+board[45]+"(45)"+"-------------"+board[46]+"(46)"+"-------------"+board[47]+"(47)"+"         |         |      |         |         |")
	print("|         |         |      |         "+board[37]+"(37)"+"-----------------------"+board[38]+"(38)"+"-----------------------"+board[39]+"(39)"+"         |      |         |         |") 
	print("|         |         |      "+board[29]+"(29)"+"---------------------------------"+board[30]+"(31)"+"---------------------------------"+board[32]+"(32)"+"      |         |         |")
	print("|         |         "+board[21]+"(21)"+"----------------------------------------"+board[22]+"(22)"+"----------------------------------------"+board[18]+"(23)"+"         |         |")
	print("|         "+board[13]+"(13)"+"--------------------------------------------------"+board[14]+"(14)"+"--------------------------------------------------"+board[15]+"(15)"+"         |")
	print(board[5]+"(05)"+"------------------------------------------------------------"+board[6]+"(06)"+"------------------------------------------------------------"+board[7]+"(07)")

# Check Next Mill
def checkNextMill_six(position, board, player):
    mill = [
        (isMill(player, board, 1, 2) or isMill(player, board, 3, 5)),#0
        (isMill(player, board, 0, 2) ),#1
        (isMill(player, board, 0, 1) or isMill(player, board, 4, 7)),#2
        (isMill(player, board, 0, 5) ),#3
        (isMill(player, board, 2, 7) ),#4
        (isMill(player, board, 0, 3) or isMill(player, board, 6, 7)),#5
        (isMill(player, board, 5, 7) ),#6
        (isMill(player, board, 2, 4) or isMill(player, board, 5, 6)),#7
        (isMill(player, board, 9, 10) or isMill(player, board, 11, 13)),#8
        (isMill(player, board, 8, 10) ),#9
        (isMill(player, board, 8, 9) or isMill(player, board, 12, 15)),#10
        (isMill(player, board, 8, 13)),#11
        (isMill(player, board, 10, 15)),#12
        (isMill(player, board, 8, 11) or isMill(player, board, 14, 15)),#13
        (isMill(player, board, 13, 15)),#14
        (isMill(player, board, 13, 14) or isMill(player, board, 10, 12))#15
    ]

def checkNextMill_nine(position, board, player):
    mill = [
        (isMill(player, board, 1, 2) or isMill(player, board, 3, 5)),
        (isMill(player, board, 0, 2) or isMill(player, board, 9, 17)),
        (isMill(player, board, 0, 1) or isMill(player, board, 4, 7)),
        (isMill(player, board, 0, 5) or isMill(player, board, 11, 19)),
        (isMill(player, board, 2, 7) or isMill(player, board, 12, 20)),
        (isMill(player, board, 0, 3) or isMill(player, board, 6, 7)),
        (isMill(player, board, 5, 7) or isMill(player, board, 14, 22)),
        (isMill(player, board, 2, 4) or isMill(player, board, 5, 6)),
        (isMill(player, board, 9, 10) or isMill(player, board, 11, 13)),
        (isMill(player, board, 8, 10) or isMill(player, board, 1, 17)),
        (isMill(player, board, 8, 9) or isMill(player, board, 12, 15)),
        (isMill(player, board, 3, 19) or isMill(player, board, 8, 13)),
        (isMill(player, board, 20, 4) or isMill(player, board, 10, 15)),
        (isMill(player, board, 8, 11) or isMill(player, board, 14, 15)),
        (isMill(player, board, 13, 15) or isMill(player, board, 6, 22)),
        (isMill(player, board, 13, 14) or isMill(player, board, 10, 12)),
        (isMill(player, board, 17, 18) or isMill(player, board, 19, 21)),
        (isMill(player, board, 1, 9) or isMill(player, board, 16, 18)),
        (isMill(player, board, 16, 17) or isMill(player, board, 20, 23)),
        (isMill(player, board, 16, 21) or isMill(player, board, 3, 11)),
        (isMill(player, board, 12, 4) or isMill(player, board, 18, 23)),
        (isMill(player, board, 16, 19) or isMill(player, board, 22, 23)),
        (isMill(player, board, 6, 14) or isMill(player, board, 21, 23)),
        (isMill(player, board, 18, 20) or isMill(player, board, 21, 22))
    ]

    return mill[position]

def checkNextMill_twelve(position, board, player):
    mill = [
        (isMill(player, board, 1, 2) or isMill(player, board, 3, 5)),#0
        (isMill(player, board, 0, 2) or isMill(player, board, 9, 17)),#1
        (isMill(player, board, 0, 1) or isMill(player, board, 4, 7)),#2
        (isMill(player, board, 0, 5) or isMill(player, board, 11, 19)),#3
        (isMill(player, board, 2, 7) or isMill(player, board, 12, 20)),#4
        (isMill(player, board, 0, 3) or isMill(player, board, 6, 7)),#5
        (isMill(player, board, 5, 7) or isMill(player, board, 14, 22)),#6
        (isMill(player, board, 2, 4) or isMill(player, board, 5, 6)),#7
        (isMill(player, board, 9, 10) or isMill(player, board, 11, 13))#8,
        (isMill(player, board, 8, 10) or isMill(player, board, 1, 17) or isMill(player, board, 17, 25) )#9,
        (isMill(player, board, 8, 9) or isMill(player, board, 12, 15))#10,
        (isMill(player, board, 3, 19) or isMill(player, board, 8, 13) or isMill(player, board, 19, 27)),#11
        (isMill(player, board, 20, 4) or isMill(player, board, 10, 15) or isMill(player, board, 20, 28)),#12
        (isMill(player, board, 8, 11) or isMill(player, board, 14, 15)),#13
        (isMill(player, board, 13, 15) or isMill(player, board, 6, 22) or isMill(player, board,22,30)),#14
        (isMill(player, board, 13, 14) or isMill(player, board, 10, 12)),#15
        (isMill(player, board, 17, 18) or isMill(player, board, 19, 21)),#16
        (isMill(player, board, 1, 9) or isMill(player, board, 16, 18) or isMill(player, board,9,25)),#17
        (isMill(player, board, 16, 17) or isMill(player, board, 20, 23)),#18
        (isMill(player, board, 16, 21) or isMill(player, board, 3, 11) or isMill(player, board, 11, 27)),#19
        (isMill(player, board, 12, 4) or isMill(player, board, 18, 23) or isMill(player, board, 13, 28)),#20
        (isMill(player, board, 16, 19) or isMill(player, board, 22, 23)),#21
        (isMill(player, board, 6, 14) or isMill(player, board, 21, 23) or isMill(player, board,14,30)),#22
        (isMill(player, board, 18, 20) or isMill(player, board, 21, 22)),#23
        (isMill(player, board, 25, 26) or isMill(player, board, 27, 29)),#24
        (isMill(player, board, 24, 26) or  isMill(player, board,9,17)),#25
        (isMill(player, board, 24, 25) or isMill(player, board, 28, 31)),#26
        (isMill(player, board, 11,19) or isMill(player, board, 24,29)),#27
        (isMill(player, board, 12, 20) or  isMill(player, board, 26, 31)),#28
        (isMill(player, board, 30,31) or isMill(player, board, 24,27)),#29
        (isMill(player, board, 29,31) or isMill(player, board, 14, 22) ),#30
        (isMill(player, board, 29,30) or isMill(player, board, 28, 26))#31

    ]

    return mill[position]

# TODO: Add ChecknextMill for 15 and 18

# Adjacent position
adjacent_9 = [
        [1, 3], [0, 2, 9], [1, 4],
        [0, 5, 11], [2, 7, 12],
        [3, 6], [5, 7, 14],
        [4, 6], [9, 11],
        [1, 8, 10, 17], [9, 12],
        [3, 8, 13, 19],
        [4, 10, 15, 20], [11, 14],
        [6, 13, 15, 22], [12, 14],
        [17, 19], [9, 16, 18],
        [17, 20], [11, 16, 21],
        [12, 18, 23], [19, 22],
        [21, 23, 14], [20, 22]
    ]

adjacent_12 = [
        [1, 3], [0, 2, 9], [1, 4], #0, 1, 2
        [0, 5, 11], [2, 7, 12], #3,4
        [3, 6], [5, 7, 14], #5,6
        [4, 6], [9, 11], #7,8
        [1, 8, 10, 17], [9, 12], #9,10
        [3, 8, 13, 19], #11
        [4, 10, 15, 20], [11, 14], #12,13
        [6, 13, 15, 22], [12, 14], #14,15
        [17, 19], [9, 16, 18, 25], #16,17
        [17, 20], [11, 16, 21, 27], #18,19
        [12, 18, 23, 28], [19, 22], #20,21
        [14, 21, 23, 30], [20, 22], #22,23
        [25, 27], [17, 24, 26], #24,25
        [25, 28], [19, 24, 29], #26,27
        [20, 26, 31], [27, 30], #28,29
        [22, 29, 31], [28, 30] #30,31
    ]

adjacent_15 = [
        [1, 3], [0, 2, 9], [1, 4], #0, 1, 2
        [0, 5, 11], [2, 7, 12], #3,4
        [3, 6], [5, 7, 14], #5,6
        [4, 6], [9, 11], #7,8
        [1, 8, 10, 17], [9, 12], #9,10
        [3, 8, 13, 19], #11
        [4, 10, 15, 20], [11, 14], #12,13
        [6, 13, 15, 22], [12, 14], #14,15
        [17, 19], [9, 16, 18, 25], #16,17
        [17, 20], [11, 16, 21, 27], #18,19
        [12, 18, 23, 28], [19, 22], #20,21
        [14, 21, 23, 30], [20, 22], #22, 23
        [25, 27], [17, 24, 26, 33], #24, 25
        [25, 28], [19, 24, 29, 35], #26, 27
        [20, 26, 31, 36], [27, 30], #28, 29
        [22, 29, 31, 38], [28, 30], #30, 31
        [33, 35], [25, 32, 34], #32, 33
        [33, 36], [27, 32, 37], #34, 35
        [23, 34, 39], [35, 38], #36, 37
        [30, 37, 39], [36, 38] #38, 39
    ]

adjacent_18 = [
        [1, 3], [0, 2, 9], [1, 4], #0, 1, 2
        [0, 5, 11], [2, 7, 12], #3,4
        [3, 6], [5, 7, 14], #5,6
        [4, 6], [9, 11], #7,8
        [1, 8, 10, 17], [9, 12], #9,10
        [3, 8, 13, 19], #11
        [4, 10, 15, 20], [11, 14], #12,13
        [6, 13, 15, 22], [12, 14], #14,15
        [17, 19], [9, 16, 18, 25], #16,17
        [17, 20], [11, 16, 21, 27], #18,19
        [12, 18, 23, 28], [19, 22], #20,21
        [14, 21, 23, 30], [20, 22], #22,23
        [25, 27], [17, 24, 26, 33], #24,25
        [25, 28], [19, 24, 29, 35], #26,27
        [20, 26, 31, 36], [27, 30], #28,29
        [22, 29, 31, 38], [28, 30], #30,31
        [33, 35], [25, 32, 34, 41], #32,33
        [33, 36], [27, 32, 37, 43], #34,35
        [23, 34, 39, 44], [35, 38], #36, 37
        [30, 37, 39, 46], [36, 38], #38, 39
        [41, 43], [33, 40, 42], #40,41
        [41, 44], [35, 40, 45], #42, 43
        [36, 42, 47], [43, 46], #44, 45
        [38, 45, 47], [44, 46] #46, 47
    ]