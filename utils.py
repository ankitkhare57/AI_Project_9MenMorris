from copy import deepcopy

# Prints board, using board positions as a parameter
def printBoard(board):
    print(board[0] + "(00)----------------------" + board[1] +
          "(01)----------------------" + board[2] + "(02)")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|       " + board[8] + "(08)--------------" +
          board[9] + "(09)--------------" + board[10] + "(10)     |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |        " + board[16] + "(16)-----" +
          board[17] + "(17)-----" + board[18] + "(18)       |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print(board[3] + "(03)---" + board[11] + "(11)----" + board[19] + "(19)               " +
          board[20] + "(20)----" + board[12] + "(12)---" + board[4] + "(04)")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |        " + board[21] + "(21)-----" +
          board[22] + "(22)-----" + board[23] + "(23)       |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       " + board[13] + "(13)--------------" +
          board[14] + "(14)--------------" + board[15] + "(15)     |")
    print("|                           |                           |")
    print("|                           |                           |")
    print("|                           |                           |")
    print(board[5] + "(05)----------------------" + board[6] +
          "(06)----------------------" + board[7] + "(07)")
    print("\n")

# Returns a list of adjacent locations for a given location
def adjacentLocations(position):
    adjacent = [
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
    return adjacent[position]

# Function to check is a player is present on the positions p1 and p2 on the board
def isPlayer(player, board, p1, p2):
    if (board[p1] == player and board[p2] == player):
        return True
    else:
        return False

# Function that returns true if a player can make a mill in the next move 
def checkNextMill(position, board, player):
    mill = [
        (isPlayer(player, board, 1, 2) or isPlayer(player, board, 3, 5)),
        (isPlayer(player, board, 0, 2) or isPlayer(player, board, 9, 17)),
        (isPlayer(player, board, 0, 1) or isPlayer(player, board, 4, 7)),
        (isPlayer(player, board, 0, 5) or isPlayer(player, board, 11, 19)),
        (isPlayer(player, board, 2, 7) or isPlayer(player, board, 12, 20)),
        (isPlayer(player, board, 0, 3) or isPlayer(player, board, 6, 7)),
        (isPlayer(player, board, 5, 7) or isPlayer(player, board, 14, 22)),
        (isPlayer(player, board, 2, 4) or isPlayer(player, board, 5, 6)),
        (isPlayer(player, board, 9, 10) or isPlayer(player, board, 11, 13)),
        (isPlayer(player, board, 8, 10) or isPlayer(player, board, 1, 17)),
        (isPlayer(player, board, 8, 9) or isPlayer(player, board, 12, 15)),
        (isPlayer(player, board, 3, 19) or isPlayer(player, board, 8, 13)),
        (isPlayer(player, board, 20, 4) or isPlayer(player, board, 10, 15)),
        (isPlayer(player, board, 8, 11) or isPlayer(player, board, 14, 15)),
        (isPlayer(player, board, 13, 15) or isPlayer(player, board, 6, 22)),
        (isPlayer(player, board, 13, 14) or isPlayer(player, board, 10, 12)),
        (isPlayer(player, board, 17, 18) or isPlayer(player, board, 19, 21)),
        (isPlayer(player, board, 1, 9) or isPlayer(player, board, 16, 18)),
        (isPlayer(player, board, 16, 17) or isPlayer(player, board, 20, 23)),
        (isPlayer(player, board, 16, 21) or isPlayer(player, board, 3, 11)),
        (isPlayer(player, board, 12, 4) or isPlayer(player, board, 18, 23)),
        (isPlayer(player, board, 16, 19) or isPlayer(player, board, 22, 23)),
        (isPlayer(player, board, 6, 14) or isPlayer(player, board, 21, 23)),
        (isPlayer(player, board, 18, 20) or isPlayer(player, board, 21, 22))
    ]
    return mill[position]

# Return True if a player has a mill on the given position
def isMill(position, board):
    player = board[position]
    if player != 'x':
        return checkNextMill(position, board, player)
    else:
        return False

'''
Function to return number of pieces owned by a player on the board,
value is '1' or '2' (player number)
'''
def numOfPieces(board, value):
    return board.count(value)

# Checks whether all pieces owned by the player are Mill
def allIsMill(board, player):
    isMill = False
    for i in range(len(board)):
        if (board[i] == player):
            if checkNextMill(i, board, player):
                isMill = True
            else:
                return False
    return isMill

'''
Function to remove a piece from the board.
If the player is 1, then a piece of player 2 is removed, and vice versa
'''
def removePiece(board_copy, board_list, player):
    for i in range(len(board_copy)):
        if player == '1':
            opp = '2'
        else:
            opp = '1'
        if(board_copy[i] == opp):
            if not isMill(i, board_copy):
                new_board = deepcopy(board_copy)
                new_board[i] = 'x'

                # Making a new board and emptying the position where piece is removed
                board_list.append(new_board)

    return board_list

# Generating all possible moves for Stage 2 (Moving Pieces) of the game
def possibleMoves_stage2(board, player):

    board_list = []

    for i in range(len(board)):

        if(board[i] == player):
            adjacent_list = adjacentLocations(i)
            for pos in adjacent_list:
                '''
                Checks if location is empty, then moves the piece to the new location by 
                emptying the current location
                '''
                if (board[pos] == 'x'):
                    board_copy = deepcopy(board)
                    board_copy[i] = 'x'
                    board_copy[pos] = player

                    # In case of mill, remove Piece
                    if isMill(pos, board_copy):
                        board_list = removePiece(
                            board_copy, board_list, player)
                    else:
                        board_list.append(board_copy)
    return board_list


'''
Generating all possible moves for Stage 3 (Flying Condition) of the game
i.e., when one player has only 3 pieces
'''
def possibleMoves_stage3(board, player):

    board_list = []

    for i in range(len(board)):
        if(board[i] == player):
            for j in range(len(board)):
                
                # The piece can fly to any empty position, not only adjacent one
                if (board[j] == 'x'):
                    board_copy = deepcopy(board)
                    board_copy[i] = 'x'
                    board_copy[j] = player

                    # If a Mill is formed, remove piece
                    if isMill(j, board_copy):
                        
                        board_list = removePiece(
                            board_copy, board_list, player)
                    else:
                        board_list.append(board_copy)
    return board_list


# Checks if game is in Stage 2 or 3 and returns possible moves accordingly
def possibleMoves_stage2or3(board, player='1'):
    if numOfPieces(board, player) == 3:
        return possibleMoves_stage3(board, player)
    else:
        return possibleMoves_stage2(board, player)
        