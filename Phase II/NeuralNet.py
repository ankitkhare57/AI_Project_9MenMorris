from AlphaBeta import *
from BoardLogic import *
from heuristics import *
from Utility import *
import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh

def encode(arr):
    arr = np.array(arr)
    arr[arr == 'X'] = "0"
    arr = arr.astype(float)
    arr = tr.tensor([arr], dtype=tr.float32)
    return arr

def decode(x):
    board = x[0].numpy()
    board = board.astype(int)
    board = board.astype(str)
    board[board == '0'] = "X"
    board = board.tolist()
    return board

def BlockusNet1(board_size):
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