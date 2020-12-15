from AlphaBeta import *
from BoardLogic import *
from heuristics import *
from Utility import *
import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh
import random

def encode(arr):
    arr = np.array(arr)
    arr[arr == 'X'] = "0"
    arr = arr.astype(float)
    arr = tr.tensor(arr, dtype=tr.float32)
    return arr

def decode(x):
    # board = x[0].numpy()
    board = x.astype(int)
    board = board.astype(str)
    board[board == '0'] = "X"
    board[board == '1'] = "1"
    board[board == '2'] == "2"
    board = board.tolist()
    return board

def generate(board_size, num_games, max_depth, numberPlayers):
    board = []
    alpha = float('-inf')
    beta = float('inf')
    depth = 3
    ai_depth = 4
    h1 = numberOfPiecesHeuristic
    h2 = AdvancedHeuristic
    inputs = []
    outputs = []

    for games in range(num_games):
        for i in range(24):
            board.append('X')

        evaluation = evaluator()

        # Stage 1: AI 1 - Baseline
        for i in range(numberPlayers): 
            temp_empty_positions = []
            temp_positions_player2 = []

            for i in range(24):
                if board[i] == 'X':
                    temp_empty_positions.append(i)
                if board[i] == '2' and (not isMill_BaselineAI(i, board)):
                    temp_positions_player2.append(i)
        
            selected_move = random.choice(temp_empty_positions)

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
                        else:  
                            break
            
            # AI 2
            evalBoard = alphaBetaPruning(board, ai_depth, False, alpha, beta, True, h1)

            temp = evalBoard.board
            inputs.append(board)
            outputs.append(temp)
            if evalBoard.evaluator == float('-inf'):
                # alphabeta_win = 1
                return inputs, outputs
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
                    else:
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

            if isCloseMill(new_pos, board):
                userHasRemoved = False
                while not userHasRemoved:
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
                        else:
                            break

            # AI 2
            evaluation = alphaBetaPruning(board, ai_depth, False, alpha, beta, False, h2)

            temp = evaluation.board
            inputs.append(board)
            outputs.append(temp)
            if evaluation.evaluator == float('-inf'):
                # alphabeta_win = 1
                return inputs, outputs
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
                    else:
                        board[pos] = '2'
                        board[old_pos] = 'X'
                else:
                    board = temp
    print("inputs", inputs)
    return inputs, outputs

def get_batch(board_size=24, num_games=25, max_depth=6, numberPlayers=9):
    inputs, outputs = generate(board_size, num_games, max_depth, numberPlayers)
    print("data", outputs)
    inputs = encode(inputs)
    outputs = encode(outputs)
    net = NineMenMorrisNet(board_size=board_size)
    import pickle as pk
    with open("data%d.pkl" % board_size, "wb") as f: pk.dump((inputs, outputs), f)
    with open("data%d.pkl" % board_size,"rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop 
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(100):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model%d.pth" % board_size)

    # TODO: Plot learning rate


def NineMenMorrisNet(board_size):
    model = Sequential(
        Flatten(),
        Linear(board_size, 1, True)
    )
    return model

def calculate_loss(net, x, y_targ):
    y = net(x)
    e = tr.sum((y-y_targ)**2)
    return (y, e)

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return (y, e)
