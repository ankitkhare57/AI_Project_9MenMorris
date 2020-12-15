
### Steps to run the Project (Phase III):
1.  Download/Clone repository
2.  cd "Phase II" 
3.  Run main.py
4.  Select Problem Variation (number of pieces). The variation that we worked on are: 3 pieces, 4 pieces, 6 pieces, 7 pieces and 9 pieces. Please enter 3, 4, 6, 7 or 9.
5.  Choose from the 5 options: Human vs Human, Human vs Baseline AI, Human vs Tree-based AI, Human vs Tree and Neural Network AI and Train the data for Neural Network.
6.  Follow on-screen prompts.


### Steps to run the Project (Phase I):
1.  Download/Clone repository
2.  Run human_vs_human.py 
3.  Follow on-screen prompts.
    
### Dependencies: Pytorch, Numpy
**Install Pytorch:** Follow the instructions on this links: https://pytorch.org/get-started/locally/ based on the machine requirements.
**Install Numpy:** Run pip install numpy

### Imports Used: copy, sys, random

### Procedure Descriptions:

#### def printBoard(board):
**Input:** Board list <br>
**Output:** Prints the current state of the board<br>
<br>

#### def adjacentLocations(position):
**Input:** Position of the player <br>
**Output:** Returns an array of the adjacent positions for the input position <br>
**Description:** It has an array which has precalculated adjacent positions for each position, the index of the array is the position.<br>
<br>

#### def isPlayer(player, board, p1, p2):
**Input:** Current Player, Current board, two positions<br>
**Output:** Boolean value<br>
**Description:** This is a helper function for checkNextMill(), this function takes the current board and player and checks if both the positions have that same player on them.<br>
<br>

#### def checkNextMill(position, board, player):
**Input:** Position to be placed, Current board, Current Player<br>
**Output:** Boolean Value<br>
**Description:** The function checks if the player can make a mill (3 pieces in a row) in the with the move<br>
<br>

#### def isMill(position, board):
**Input:** Current position, Current board<br>
**Output:** Boolean Value<br>
**Description:** This function checks if the current position is a part of a mill or not<br>
<br>

#### def numOfPieces(board, value):
**Input:** Current board, player<br>
**Output:** Integer value<br>
**Description:** This function counts the number of pieces of a player on the board.<br>
<br>

#### def allIsMill(board, player):
**Input:** Current board, player<br>
**Output:** Boolean Value<br>
**Description:** This function checks if all the pieces for a certain player are only mills so that it can be removed by the opponent if the opponent forms a mill.<br>

#### def removePiece(board_copy, board_list, player):
**Input:** Copy of the board, Current board, Current player<br>
**Output:** Updated board (board_list)<br>
**Description:** This function updates the board by removing the piece, checks that if the opponent piece is a part of a mill or not if it is removed fails or else it passes and then the board is updated.<br>
<br>

#### def possibleMoves_stage2(board, player):
**Input:** Current Board, Current Player<br>
**Output:** board_list<br>
**Description:** This function takes the current board and the current player; it checks what are the adjacent positions and the valid positions. After which it puts an x in place of the current position and then updates the new position and then checks if it forms a mill. If it does it goes for the removal of the opponent's piece.<br>
<br>

#### def possibleMoves_stage3(board, player):
**Input:** Current Board, Current Player<br>
**Output:** board_list<br>
**Description:** This function puts an x to all the empty positions other than the opponent’s pieces as possible positions for the current player. It also checks if the current piece is forming a mill. If it forms a mill then it asks which of the opponent’s pieces has to be removed and removes it. If a mill is not formed then just updates the board. This function handles a special stage called the flying stage. In this when one of the players has only 3 pieces remaining they can not only move their pieces to adjacent positions but also to any position available on the board.<br>
<br>

#### def possibleMoves_stage2or3(board, player='1'):
**Input:** Current board and Current player<br>
**Output:** Which stage to go ahead with depending on the number of players<br>
**Description:** Checks if the number of pieces of a player is 3 then go for stage 3 else go for stage 2. This is done by calling that function for the possible moves respectively (**possibleMoves_stage3()** or **possibleMoves_stage2()**)<br>
<br>

#### def human_vs_human():
**Description:** This is the main function that uses all the above functions to implement the game. Here the probability of failing to remove an opponent's piece after forming a mill is 25% of the time. This is decided by the variable “ans” in the code.<br>
<br>

#### References:<br>
1. The Rules of Merels or Nine Men’s Morris. (2019). Retrieved October 28, 2020, from https://www.mastersofgames.com/rules/morris-rules.htm <br>
2. 9MensMorris. (2019). Retrieved October 28, 2020, from https://github.com/SidJain1412/9MensMorris<br>
3. Paszke, A., Gross, S., Chintala, S., Chanan, G., Yang, E., DeVito, Z., Lin, Z., Desmaison, A., Antiga, L., & Lerer, A. (2017). Automatic differentiation in PyTorch. In NIPS-W.<br>
4. Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 0.1038/s41586-020-2649-2. <br>
