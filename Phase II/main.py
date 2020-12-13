from AlphaBeta import *
from BoardLogic import *
from heuristics import *
from Utility import *
from NeuralNet import *
import time
import random
import sys

alpha = float('-inf')
beta = float('inf')
depth = 3
ai_depth = 4
n = 9
board_size = int((8*n)/3)
iterations = 5

def boardOutput(board):
        
        print(board[0]+"(00)----------------------"+board[1]+"(01)----------------------"+board[2]+"(02)")
        print("|                           |                           |")
        print("|       "+board[8]+"(08)--------------"+board[9]+"(09)--------------"+board[10]+"(10)     |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       |        "+board[16]+"(16)-----"+board[17]+"(17)-----"+board[18]+"(18)       |      |")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print(board[3]+"(03)---"+board[11]+"(11)----"+board[19]+"(19)               "+board[20]+"(20)----"+board[12]+"(12)---"+board[4]+"(04)")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print("|       |        "+board[21]+"(21)-----"+board[22]+"(22)-----"+board[23]+"(23)       |      |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       "+board[13]+"(13)--------------"+board[14]+"(14)--------------"+board[15]+"(15)     |")
        print("|                           |                           |")
        print("|                           |                           |")
        print(board[5]+"(05)----------------------"+board[6]+"(06)----------------------"+board[7]+"(07)")

def AI_VS_AI_NN(h1, h2):

    board = []
    for i in range(24):
        board.append('X')

    evaluation = evaluator()
    nodes_accessed = 0
    alphabeta_win = 0

    board_size = 24
    net = BlockusNet1(board_size=board_size)
    print(net)

    # Stage 1
    print("Stage 1")
    for i in range(9):

        # AI 1 - AI with NN
        import pickle as pk
        # with open("data%d.pkl" % board_size,"rb") as f: (x, y_targ) = pk.load(f)

        # Optimization loop
        x = encode(board)
        print(x)
        y_targ = encode(alphaBetaPruning(board, ai_depth, False, alpha, beta, True, h1).board)
        # print("---ytarg")
        # print(y_targ)

        optimizer = tr.optim.Adam(net.parameters())
        train_loss, test_loss = [], []
        shuffle = np.random.permutation(range(len(x)))
        split = 12
        train, test = shuffle[:-split], shuffle[-split:]
        for epoch in range(iterations):
            y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
            y_test, e_test = calculate_loss(net, x[test], y_targ[test])
            if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
            train_loss.append(e_train.item() / (len(shuffle)-split))
            test_loss.append(e_test.item() / split)
        
        tr.save(net.state_dict(), "model%d.pth" % board_size)
        
        board = decode(x)

        # AI 2
        evalBoard = alphaBetaPruning(board, ai_depth, False, alpha, beta, True, h1)
        boardOutput(board)
        
        states_reached = getStatesReached()
        print("Number of tree nodes processed: ", states_reached)
        nodes_accessed += states_reached

        temp = evalBoard.board
        if evalBoard.evaluator == float('-inf'):
            print("AI Bot 2 has won!")
            alphabeta_win = 1
            return nodes_accessed, alphabeta_win
        else:
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 1:
                    board = evalBoard.board
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
            else:
                board = temp


    # Stage 2
    userHasMoved = False
    while not userHasMoved:

        # AI 1 - AI with NN
        import pickle as pk
        # with open("data%d.pkl" % board_size,"rb") as f: (x, y_targ) = pk.load(f)

        # Optimization loop
        x = encode(board)
        print(x)
        y_targ = encode(alphaBetaPruning(board, ai_depth, False, alpha, beta, True, h1).board)
        # print("---ytarg")
        # print(y_targ)

        optimizer = tr.optim.Adam(net.parameters())
        train_loss, test_loss = [], []
        shuffle = np.random.permutation(range(len(x)))
        split = 12
        train, test = shuffle[:-split], shuffle[-split:]
        for epoch in range(iterations):
            y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
            y_test, e_test = calculate_loss(net, x[test], y_targ[test])
            if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
            train_loss.append(e_train.item() / (len(shuffle)-split))
            test_loss.append(e_test.item() / split)
        
        tr.save(net.state_dict(), "model%d.pth" % board_size)
        board = decode(x)

        # AI 2
        evaluation = alphaBetaPruning(board, ai_depth, False, alpha, beta, False, h2)

        states_reached = getStatesReached()
        boardOutput(board)
        print("Number of tree nodes processed: ", states_reached)
        nodes_accessed += states_reached

        temp = evaluation.board
        if evaluation.evaluator == float('-inf'):
            print("AI Bot 2 has WON!")
            alphabeta_win = 1
            return nodes_accessed, alphabeta_win
        else:
            pos = old_pos = 0
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break

                for j in range(24):
                    if board[j] == '2' and temp[j] == 'X':
                        old_pos = j
                        break

                arr = [1, 1, 1, 0]
                ans = random.choice(arr)

                if ans == 1:
                    board = temp
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
                    board[old_pos] = 'X'
            else:
                board = temp

    return nodes_accessed, alphabeta_win    

def AI_VS_AI(h1, h2):

    board = []
    for i in range(24):
        board.append('X')

    # boardOutput(board)

    evaluation = evaluator()
    nodes_accessed = 0
    alphabeta_win = 0

    # Stage 1: AI 1 - Baseline
    print("Stage 1")
    for i in range(9):
    
        temp_empty_positions = []
        temp_positions_player2 = []

        for i in range(24):
            if board[i] == 'X':
                temp_empty_positions.append(i)
            if board[i] == '2' and (not isMill_BaselineAI(i, board)):
                temp_positions_player2.append(i)
    
        selected_move = random.choice(temp_empty_positions)
        print('Player AI plays at', selected_move)
        board[selected_move] = '1'
        if isCloseMill(selected_move, board):
            itemPlaced = False
            while not itemPlaced:
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 1:
                    ans = 0.75
                else: 
                    ans = 0.25
                selected_move = random.choice(temp_positions_player2)
                if board[selected_move] == '2' and not isCloseMill(selected_move, board) or allIsMill(board, '2'):
                    if ans == 0.75:
                        board[selected_move] = 'X'
                        itemPlaced = True
                        print("Probability of removing Player '2\'s' piece", ans)
                        print("Remove Successful at position ", selected_move)
                    else:  
                        print("Probability of removing Player '2\'s' piece", ans)
                        print("Cannot Remove. Player '2\'s' turn")
                        break

        
        # AI 2
        evalBoard = alphaBetaPruning(board, ai_depth, False, alpha, beta, True, h1)
        # boardOutput(board)
        
        states_reached = getStatesReached()
        print("Number of tree nodes processed: ", states_reached)
        nodes_accessed += states_reached

        temp = evalBoard.board
        if evalBoard.evaluator == float('-inf'):
            print("AI Bot 2 has won!")
            alphabeta_win = 1
            return nodes_accessed, alphabeta_win
        else:
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 1:
                    board = evalBoard.board
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
            else:
                board = temp



    # Stage 2: BaseLine AI
    userHasMoved = False
    while not userHasMoved:
        player1_positions = []
        player1_poss = []

        for i in range(len(board)):
            if board[i] == '1':
                player1_positions.append(i)
                adj_pos = adjacentLocations(i)
                temp = []
                for pos in adj_pos:
                    if board[pos] == 'X':
                        temp.append(pos)
                player1_poss.append(temp)

        selected = False

        while not selected:
            idx_player_to_move = random.choice(range(len(player1_positions)))
            possible_loc = player1_poss[idx_player_to_move]
            if len(possible_loc) > 0:
                new_pos = random.choice(possible_loc)
                selected = True

        
        board[player1_positions[idx_player_to_move]] = 'X'
        board[new_pos] = '1'
        print('Baseline AI has moved from '+str(player1_positions[idx_player_to_move])+' to '+str(new_pos))
        # boardOutput(board)
        if isCloseMill(new_pos, board):
            print('BaseLine AI Forms Mill at position', new_pos)
            userHasRemoved = False
            while not userHasRemoved:
                # boardOutput(board)
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 0:
                    ans = 0.25
                else: 
                    ans = 0.75

                temp_positions_player2 = []
                for i in range(24):
                    if board[i] == '2' and (not isMill_BaselineAI(i, board)):
                        temp_positions_player2.append(i)

                selected_remove = random.choice(temp_positions_player2)
                if board[selected_remove] == '2' and not isCloseMill(selected_remove, board) or allIsMill(board, '2'):
                    if ans == 0.75:
                        board[selected_remove] = 'X'
                        userHasRemoved = True
                        
                        print("Probability of removing Player '2\'s' piece", ans)
                        print("Remove Successful at position", selected_move)
                    else:
                        print("Probability of removing Player '2\'s' piece", ans)
                        print("Cannot Remove. Player '2\'s' turn")
                        break

            # print('Player AI removed 1\'s at', selected_remove)

        # userHasMoved = True   
        # boardOutput(board)    
    # --------------------------------------------------
        if(len(stage23Moves(board)) == 0):
            print("-----------")
            print("    TIE    ")
            print("-----------")
            return nodes_accessed, alphabeta_win
            # sys.exit()

        elif numOfValue(board, '2') < 3:
            print("Baseline AI WINS!")
            return nodes_accessed, alphabeta_win
            # sys.exit()

        # AI 2
        evaluation = alphaBetaPruning(board, ai_depth, False, alpha, beta, False, h2)

        
        states_reached = getStatesReached()
        # boardOutput(board)
        print("Number of tree nodes processed: ", states_reached)
        nodes_accessed += states_reached

        temp = evaluation.board
        if evaluation.evaluator == float('-inf'):
            print("AI Bot 2 has WON!")
            alphabeta_win = 1
            return nodes_accessed, alphabeta_win
        else:
            pos = old_pos = 0
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break

                for j in range(24):
                    if board[j] == '2' and temp[j] == 'X':
                        old_pos = j
                        break

                arr = [1, 1, 1, 0]
                ans = random.choice(arr)

                if ans == 1:
                    board = temp
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
                    board[old_pos] = 'X'
            else:
                board = temp

    return nodes_accessed, alphabeta_win


def HUMAN_VS_AI(heuristic_stage1, heuristic_stage23):
    
    board = []
    print("Enter number of pieces")
    numberPlayers = int(input())
    for i in range(24):
        board.append('X')

    evaluation = evaluator()
        
    for i in range(numberPlayers):

        boardOutput(board)
        finished = False
        while not finished:
            try:

                pos = int(input("\nPlace '1' piece: ")) 
                
                if board[pos] == 'X':
                    
                    board[pos] = '1'
                    if isCloseMill(pos, board):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                arr = [1, 1, 1, 0]
                                ans = random.choice(arr)
                                if ans == 1:
                                    ans = 0.75
                                else:
                                    ans = 0.25
                                pos = int(input("\nRemove '2' piece: "))
                                
                                if board[pos] == '2' and not isCloseMill(pos, board) or allIsMill(board, '2'):
                                    if ans == 0.75:
                                        board[pos] = 'X'
                                        itemPlaced = True
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Remove Successful")
                                    else:
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Cannot Remove. Player '2\'s' turn")
                                        break
                                else:
                                    print("Invalid position")
                                    
                            except Exception:
                                print("Input was either out of bounds or wasn't an integer")

                    finished = True

                else:
                    print("There is already a piece there")

            except Exception:
                print("Couldn't get the input value")
        
        boardOutput(board)

        evalBoard = alphaBetaPruning(board, depth, False, alpha, beta, True, heuristic_stage1)
        
        temp = evalBoard.board
        if evalBoard.evaluator == float('-inf'):
            print("AI WINS!")
            exit(0)
        else:
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 1:
                    board = evalBoard.board
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
            else:
                board = temp

    # Stage 2: Player 1
    print('STAGE 2:-')
    while True:
        boardOutput(board)
        userMoved = False
        while not userMoved:
            try:
                movable = False
                if numOfValue(board, '1') == 3:
                    only3 = True
                else:
                    only3 = False

                while not movable:
                    pos1 = int(input("\nPLAYER '1': Which '1\'s' piece will you move?: "))

                    # Exit Program
                    # if pos1 == 'exit':
                    #   sys.exit()
                    # pos1 = int(pos1)

                    while board[pos1] != '1':
                        print("Invalid. Try again.")
                        pos1 = int(input("\nPLAYER '1': Which '1\'s' piece will you move?: "))

                        # Exit Program
                        # if pos1 == 'exit':
                        #   sys.exit()
                        # pos1 = int(pos1)

                    if only3:
                        movable = True
                        print("Stage 3 for Player '1'. Allowed to Fly")
                        break

                    possibleMoves = adjacentLocations(pos1)

                    for adjpos in possibleMoves:
                        if board[adjpos] == 'X':
                            movable = True
                            break
                    if movable == False:
                        print("No empty adjacent pieces!")

                userPlaced = False

                while not userPlaced:
                    newpos1 = int(input("'1\'s' New Position is : "))

                    # Exit Program
                    # if newpos1 == 'exit':
                    #   sys.exit()
                    # newpos1 = int(newpos1)

                    if newpos1 in adjacentLocations(pos1) or only3:
                        if board[newpos1] == 'X':
                            board[pos1] = 'X'
                            board[newpos1] = '1'
                            boardOutput(board)

                            if isCloseMill(newpos1, board):
                                userRemoved = False

                                while not userRemoved:
                                    try:
                                        arr = [1, 1, 1, 0]
                                        ans = random.choice(arr)
                                        if ans == 0:
                                            ans = 0.25
                                        else: 
                                            ans = 0.75

                                        removepos1 = int(input("\nA Mill is Formed. Remove Player '2\'s' piece: "))

                                        # Exit Program
                                        # if removepos1 == 'exit':
                                        #   sys.exit()
                                        # removepos1 = int(removepos1)

                                        if board[removepos1] == '2' and not isCloseMill(removepos1, board) or allIsMill(board, '2'):
                                            if ans == 0.75:
                                                board[removepos1] = 'X'
                                                userRemoved = True
                                                boardOutput(board)
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Remove Successful")
                                            else:
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Cannot Remove. Player '2\'s' turn")
                                                break
                                        else:
                                            print("Invalid Position")

                                    except Exception as e:
                                        print(str(e))
                                        print("Error while accepting input")

                            userPlaced = True
                            userMoved = True

                        else:
                            print('Invalid Position')


                    else:
                        print("Only adjacent locations in Stage 2. Try again.")

            except Exception as e:
                print(str(e))

       # printBoard(board)

        if(len(stage23Moves(board)) == 0):
            print("-----------")
            print("    TIE    ")
            print("-----------")
            sys.exit()

        elif numOfValue(board, '2') < 3:
            print("PLAYER '1' WINS")
            sys.exit()


        # Stage 2: Player 2
        evaluation = alphaBetaPruning(board, depth, False, alpha, beta, False, heuristic_stage23)
        
        temp = evaluation.board
        if evaluation.evaluator == float('-inf'):
            print("AI WINS")
            exit(0)
        else:
            human_pieces = numOfValue(board, '1')
            human_pieces_ai = numOfValue(temp, '1')
            if human_pieces_ai - human_pieces < 0:
                for i in range(24):
                    if board[i] == 'X' and temp[i] == '2':
                        pos = i
                        break

                for i in range(24):
                    if board[i] == '2' and temp[i] == 'X':
                        old_pos = i
                        break


                arr = [1, 1, 1, 0]
                ans = random.choice(arr)

                if ans == 1:
                    board = temp
                    print("Removal Successful")
                else:
                    print("Removal Unsuccessful")
                    board[pos] = '2'
                    board[old_pos] = 'X'
            else:
                board = temp


def HUMAN_VS_AIBaseline(numberPlayers):
    board = []
    for i in range(24):
        board.append('X')

    boardOutput(board)
    for i in range(numberPlayers):

        # Stage 1: Player 1
        finished = False
        while not finished:
            try:
                pos = int(input("\nPlace '1' piece: "))
                print()

                if board[pos] == 'X':
                    board[pos] = '1'

                    if isCloseMill(pos, board):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                arr = [1, 1, 1, 0]
                                ans = random.choice(arr)
                                if ans == 1:
                                    ans = 0.75
                                else:
                                    ans = 0.25
                                    
                                boardOutput(board)
                                pos = int(input("\nA Mill is Formed.\nRemove Player 2's piece: "))

                                if board[pos] == '2' and not isCloseMill(pos, board) or allIsMill(board, '2'):
                                    if ans == 0.75:
                                        board[pos] = 'X'
                                        itemPlaced = True
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Remove Successful")
                                    else:
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Cannot Remove. Player '2\'s' turn")
                                        break
                                else:
                                    print("Invalid position! Try Again!")
                                    
                            except Exception as e:
                                print("Input out of bounds")
                                print(str(e))

                    finished = True
                    boardOutput(board)
                else:
                    print("There is already a piece in position", pos)

            except Exception as e:
                print("Couldn't get the input value!")
                print(str(e))
        
        # if getEvaluationStage23(board) == float('-inf'):
        #   print("You Lost!")
        #   exit(0)

        # Stage 1: Player 2

        temp_empty_positions = []
        temp_positions_player1 = []


        allMill = allIsMill(board, '1')
        for i in range(24):
            if board[i] == 'X':
                temp_empty_positions.append(i)
            if allMill and board[i] == '1':
                temp_positions_player1.append(i)
            if not allMill and board[i] == '1' and not isMill_BaselineAI(i, board):
                temp_positions_player1.append(i)

            # if (board[i] == '1' and (not allIsMill(board, '1'))) or (board[i] == '1' and allIsMill(board, '1')):
                

        selected_move = random.choice(temp_empty_positions)
        print('Player AI plays at', selected_move)
        board[selected_move] = '2'
        if isCloseMill(selected_move, board):
            itemPlaced = False
            while not itemPlaced:
                arr = [1, 1, 1, 0]
                ans = random.choice(arr)
                if ans == 1:
                    ans = 0.75
                else: 
                    ans = 0.25
                selected_move = random.choice(temp_positions_player1)
                print(selected_move)
                # if board[selected_move] == '1' and not isCloseMill(selected_move, board) or allIsMill(board, '1'):
                if board[selected_move] == '1':
                    if ans == 0.75:
                        board[selected_move] = 'X'
                        itemPlaced = True
                        print("Probability of removing Player '1\'s' piece", ans)
                        print("Remove Successful at position ", selected_move)
                    else:  
                        print("Probability of removing Player '1\'s' piece", ans)
                        print("Cannot Remove. Player '1\'s' turn")
                        break

        boardOutput(board)

    # Stage 2: Player 1---------------------------------------------------------------------
    print('STAGE 2:-')

    while True:
        boardOutput(board)
        userMoved = False
        while not userMoved:
            try:
                movable = False
                if numOfValue(board, '1') == 3:
                    only3 = True
                else:
                    only3 = False

                while not movable:
                    pos1 = int(input("\nPLAYER '1': Which '1\'s' piece will you move?: "))

                    # Exit Program
                    # if pos1 == 'exit':
                    #   sys.exit()
                    # pos1 = int(pos1)

                    while board[pos1] != '1':
                        print("Invalid. Try again.")
                        pos1 = int(input("\nPLAYER '1': Which '1\'s' piece will you move?: "))

                        # Exit Program
                        # if pos1 == 'exit':
                        #   sys.exit()
                        # pos1 = int(pos1)

                    if only3:
                        movable = True
                        print("Stage 3 for Player '1'. Allowed to Fly")
                        break

                    possibleMoves = adjacentLocations(pos1)

                    for adjpos in possibleMoves:
                        if board[adjpos] == 'X':
                            movable = True
                            break
                    if movable == False:
                        print("No empty adjacent pieces!")

                userPlaced = False

                while not userPlaced:
                    newpos1 = int(input("'1\'s' New Position is : "))

                    # Exit Program
                    # if newpos1 == 'exit':
                    #   sys.exit()
                    # newpos1 = int(newpos1)

                    if newpos1 in adjacentLocations(pos1) or only3:
                        if board[newpos1] == 'X':
                            board[pos1] = 'X'
                            board[newpos1] = '1'
                            boardOutput(board)

                            if isCloseMill(newpos1, board):
                                userRemoved = False

                                while not userRemoved:
                                    try:
                                        arr = [1, 1, 1, 0]
                                        ans = random.choice(arr)
                                        if ans == 0:
                                            ans = 0.25
                                        else: 
                                            ans = 0.75

                                        removepos1 = int(input("\nA Mill is Formed. Remove Player '2\'s' piece: "))

                                        # Exit Program
                                        # if removepos1 == 'exit':
                                        #   sys.exit()
                                        # removepos1 = int(removepos1)

                                        if board[removepos1] == '2' and not isCloseMill(removepos1, board) or allIsMill(board, '2'):
                                            if ans == 0.75:
                                                board[removepos1] = 'X'
                                                userRemoved = True
                                                boardOutput(board)
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Remove Successful")
                                            else:
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Cannot Remove. Player '2\'s' turn")
                                                break
                                        else:
                                            print("Invalid Position")

                                    except Exception as e:
                                        print(str(e))
                                        print("Error while accepting input")

                            userPlaced = True
                            userMoved = True

                        else:
                            print('Invalid Position')


                    else:
                        print("Only adjacent locations in Stage 2. Try again.")

            except Exception as e:
                print(str(e))

       # printBoard(board)

        if(len(stage23Moves(board)) == 0):
            print("-----------")
            print("    TIE    ")
            print("-----------")
            sys.exit()

        elif numOfValue(board, '2') < 3:
            print("PLAYER '1' WINS")
            sys.exit()

        # boardOutput(board)


        # Stage 2: Player 2 ------------------------------------------------------------------------------------------
        # endStagesFinished = False
        # boardOutput(board)
        
        #Get the users next move
        userHasMoved = False
        while not userHasMoved:
            player2_positions = []
            player2_poss = []

            for i in range(len(board)):
                if board[i] == '2':
                    player2_positions.append(i)
                    adj_pos = adjacentLocations(i)
                    temp = []
                    for pos in adj_pos:
                        if board[pos] == 'X':
                            temp.append(pos)
                    player2_poss.append(temp)

            selected = False

            new_pos = idx_player_to_move = 0
            while not selected:
                idx_player_to_move = random.choice(range(len(player2_positions)))
                possible_loc = player2_poss[idx_player_to_move]
                if len(possible_loc) > 0:
                    new_pos = random.choice(possible_loc)
                    if board[new_pos] == 'X':
                        selected = True

            
            board[player2_positions[idx_player_to_move]] = 'X'
            board[new_pos] = '2'
            print('Player AI has moved from '+str(player2_positions[idx_player_to_move])+' to '+str(new_pos))
            # boardOutput(board)
            if isCloseMill(new_pos, board):
                print('Player AI Forms Mill at position', new_pos)
                userHasRemoved = False
                while not userHasRemoved:
                    boardOutput(board)
                    arr = [1, 1, 1, 0]
                    ans = random.choice(arr)
                    if ans == 0:
                        ans = 0.25
                    else: 
                        ans = 0.75
                    temp_positions_player1 = []

                    for i in range(24):
                        # if board[i] == 'X':
                        #   temp_empty_positions.append(i)
                        if allMill and board[i] == '1':
                            temp_positions_player1.append(i)
                        if not allMill and board[i] == '1' and not isMill_BaselineAI(i, board):
                            temp_positions_player1.append(i)

                    # for i in range(24):
                    #   if board[i] == '1' and (not isMill_BaselineAI(i, board)):
                    #       temp_positions_player1.append(i)

                    # selected_remove = random.choice(temp_positions_player1)
                    selected_move = random.choice(temp_positions_player1)
                    print(selected_move)
                    # if board[selected_remove] == '1' and not isCloseMill(selected_remove, board) or allIsMill(board, '1'):
                    # if board[selected_remove] == '1' and not isCloseMill(selected_remove, board) or allIsMill(board, '1'):
                    if ans == 0.75:
                        board[selected_remove] = 'X'
                        userHasRemoved = True
                        print("Probability of removing Player '1\'s' piece", ans)
                        print("Remove Successful at position", selected_move)
                    else:
                        print("Probability of removing Player '1\'s' piece", ans)
                        print("Cannot Remove. Player '1\'s' turn")
                        break

                # print('Player AI removed 1\'s at', selected_remove)

            userHasMoved = True 
            boardOutput(board)  
        # --------------------------------------------------
            if(len(stage23Moves(board)) == 0):
                print("-----------")
                print("    TIE    ")
                print("-----------")
                sys.exit()

        # if getEvaluationStage23(board) == float('-inf'):
        #   print("Player 2 WINS!")
        #   exit(0)

            elif numOfValue(board, '1') < 3:
                print("PLAYER '2'(BaselineAI) WINS")
                sys.exit() 


if __name__ == "__main__":
    
    print("Welcome to Nine Mens Morris")
    print("===========================")
    print("1. Human vs Baseline AI")
    print("2. Human vs Tree-based AI")
    print("3. Baseline AI vs Tree-based AI")
    print("4. Simulate Baseline AI vs Tree-based AI x 100 & plot")
    print("5. AI vs AI NN")

    gametype = int(input("Please enter 1 or 2 or 3 or 4: "))

    while gametype != 1 and gametype != 2 and gametype != 3 and gametype != 4 and gametype != 5:
        gametype = int(input("Please enter 1 or 2 or 3 or 4"))

    if gametype == 1:
            print("Enter number of pieces")
            numberPlayers = int(input())
            HUMAN_VS_AIBaseline(numberPlayers)
    elif gametype == 2:
        HUMAN_VS_AI(numberOfPiecesHeuristic, AdvancedHeuristic)
    elif gametype == 3:
        AI_VS_AI(numberOfPiecesHeuristic, AdvancedHeuristic)
    elif gametype == 4:
        nodes_arr = []
        winners_arr = []
        for i in range(5):
            nodes, winner = AI_VS_AI(numberOfPiecesHeuristic, AdvancedHeuristic)
            nodes_arr.append(nodes)
            winners_arr.append(winner)
            print("Game " + str(i+1) + " finished!")
            print("Nodes Per Game: ", nodes)
            print("Winner ", winner)
        print("Nodes Array: ", nodes_arr)
        print("Winner Array: ", winners_arr)
    elif gametype == 5:
        AI_VS_AI_NN(numberOfPiecesHeuristic, AdvancedHeuristic)



        
