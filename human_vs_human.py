from utils import printBoard, isMill, numOfPieces, adjacentLocations, possibleMoves_stage2or3, allIsMill
import sys, random

def human_vs_human():
    board = []
    for i in range(24):
        board.append('x')

    printBoard(board)

    print("STAGE 1 (Place)")
    for i in range(9):

        # FOR PLAYER 1, STAGE 1-------------------------------------
        finished1 = False
        while not finished1:
            try:
                pos1 = input("\nPLAYER '1': Place a piece at: ")
                print()

                # Exit the program
                if pos1 == 'exit':
                    sys.exit()
                else:
                    pos1 = int(pos1)

                if board[pos1] == 'x':
                    board[pos1] = '1'
                    if isMill(pos1, board):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                arr = [1, 1, 1, 0]
                                ans = random.choice(arr)
                                if ans == 1:
                                    ans = 0.75
                                else: 
                                    ans = 0.25
                                printBoard(board)
                                pos2 = input('\nA Mill is formed.\nRemove Player "2\'s" piece: ')

                                # Exit Program
                                if pos2 == 'exit':
                                    sys.exit()
                                pos2 = int(pos2)

                                if (board[pos2] == '2' and not isMill(pos2, board)) or allIsMill(board, '2'):
                                    if ans == 0.75:
                                        board[pos2] = 'x'
                                        itemPlaced = True
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Remove Successful")
                                    else:  
                                        print("Probability of removing Player '2\'s' piece", ans)
                                        print("Cannot Remove. Player '2\'s' turn")
                                        break
                                else:
                                    # print("Probability of remomoving Player '2\'s' piece", ans)
                                    print("Invalid Position! Try again!")
                                    
                            except Exception as e:
                                print("Input out of bounds")
                                print(str(e))

                    finished1 = True
                    printBoard(board)

                else:
                    print("There is already a piece in position ",pos1)
                    
            except Exception as e:
                print("Couldn't get the input value!")
                print(str(e))

        

        # FOR PLAYER 2, STAGE 1-------------------------------------
        finished2 = False
        while not finished2:
            try:
                pos1 = input("\nPLAYER '2': Place a piece at: ")
                print()

                # Exit Program
                if pos1 == 'exit':
                    sys.exit()
                pos1 = int(pos1)

                if board[pos1] == 'x':
                    board[pos1] = '2'
                    if isMill(pos1, board):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                arr = [1, 1, 1, 0]
                                ans = random.choice(arr)
                                if ans == 1:
                                    ans = 0.75
                                else: 
                                    ans = 0.25
                                printBoard(board)
                                pos2 = input('\nA Mill is formed.\nRemove Player "1\'s" piece: ')

                                # Exit Program
                                if pos2 == 'exit':
                                    sys.exit()
                                pos2 = int(pos2)
                                
                                if (board[pos2] == '1' and not isMill(pos2, board)) or allIsMill(board, '1'):
                                    if ans == 0.75:
                                        board[pos2] = 'x'
                                        print("Probability of removing Player \"1's\" piece", ans)
                                        itemPlaced = True
                                        print("Remove Successful")
                                    else:  
                                        print("Probability of removing Player \"1's\" piece", ans)
                                        print("Cannot Remove. Player '1\'s' turn")
                                        break
                                else:
                                    print("Probability of removing Player \"1's\" piece", ans)
                                    print("Invalid Position! Try again!")
                                    
                            except Exception as e:
                                print("Input out of bounds")
                                print(str(e))

                    finished2 = True
                    printBoard(board)
                else:
                    print("There is already a piece in position ", pos1)
                
            except Exception as e:
                print("Couldn't get the input value!")
                print(str(e))

    print('\n')
    print("STAGE 2 (Move)")
    print('\n')

    printBoard(board)

    while True:
        # PLAYER 1 STAGE 2 (MOVE)
        userMoved = False
        while not userMoved:
            try:
                movable = False

                if numOfPieces(board, '1') == 3:
                    only3 = True
                else:
                    only3 = False

                while not movable:
                    pos1 = input("\nPLAYER '1': Which '1\'s' piece will you move?: ")

                    # Exit Program
                    if pos1 == 'exit':
                        sys.exit()
                    pos1 = int(pos1)

                    while board[pos1] != '1':
                        print("Invalid. Try again.")
                        pos1 = input("\nPLAYER '1': Which '1\'s' piece will you move?: ")

                        # Exit Program
                        if pos1 == 'exit':
                            sys.exit()
                        pos1 = int(pos1)

                    if only3:
                        movable = True
                        print("Stage 3 for Player '1'. Allowed to Fly")
                        break

                    possibleMoves = adjacentLocations(pos1)

                    for adjpos in possibleMoves:
                        if board[adjpos] == 'x':
                            movable = True
                            break
                    if movable == False:
                        print("No empty adjacent pieces!")

                userPlaced = False

                while not userPlaced:
                    newpos1 = input("'1\'s' New Position is : ")

                    # Exit Program
                    if newpos1 == 'exit':
                        sys.exit()
                    newpos1 = int(newpos1)

                    if newpos1 in adjacentLocations(pos1) or only3:

                        if board[newpos1] == 'x':
                            board[pos1] = 'x'
                            board[newpos1] = '1'
                            printBoard(board)

                            if isMill(newpos1, board):
                                userRemoved = False

                                while not userRemoved:
                                    try:
                                        arr = [1, 1, 1, 0]
                                        ans = random.choice(arr)
                                        if ans == 0:
                                            ans = 0.25
                                        else: 
                                            ans = 0.75
                                        # printBoard(board)
                                        removepos1 = input("\nA Mill is Formed. Remove Player '2\'s' piece: ")

                                       	# Exit Program
                                        if removepos1 == 'exit':
                                            sys.exit()
                                        removepos1 = int(removepos1)

                                        if board[removepos1] == '2' and not isMill(removepos1, board) or allIsMill(board, '2'):
                                            if ans == 0.75:
                                                board[removepos1] = 'x'
                                                userRemoved = True
                                                printBoard(board)
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Remove Successful")
                                            else:
                                                print("Probability of removing Player '2\'s' piece", ans)
                                                print("Cannot Remove. Player '2\'s' turn")
                                                break
                                        else:
                                            print("Invalid Position")
                                            # print("Probability of removing Player 2's piece", ans)

                                    except Exception as e:
                                        print(str(e))
                                        print("Error while accepting input")

                            userPlaced = True
                            userMoved = True
                            # printBoard(board)

                        else:
                            print("Invalid Position")

                    else:
                        print("Only adjacent locations in Stage 2. Try again.")

            except Exception as e:
                print(str(e))

        # printBoard(board)

        if(len(possibleMoves_stage2or3(board, '1')) == 0):
            print("-----------")
            print("    TIE    ")
            print("-----------")
            sys.exit()

        elif numOfPieces(board, '2') < 3:
            print("PLAYER '1' WINS")
            sys.exit()

        # PLAYER 2 STAGE 2 MOVE
        userMoved = False
        while not userMoved:
            try:
                movable = False

                if numOfPieces(board, '2') == 3:
                    only3 = True
                else:
                    only3 = False

                while not movable:
                    pos1 = input("\nPLAYER '2': Which '2\'s' piece will you move?: ")

                    # Exit Program
                    if pos1 == 'exit':
                        sys.exit()
                    pos1 = int(pos1)

                    while board[pos1] != '2':
                        print("Invalid. Try again.")
                        pos1 = input("\nPLAYER '2': Which '2\'s' piece will you move?: ")

                        # Exit Program
                        if pos1 == 'exit':
                            sys.exit()
                        pos1 = int(pos1)

                    if only3:
                        movable = True
                        print("Stage 3 for Player '2'. Allowed to Fly")
                        break

                    possibleMoves = adjacentLocations(pos1)

                    for adjpos in possibleMoves:
                        if board[adjpos] == 'x':
                            movable = True
                            break
                    if movable == False:
                        print("No empty adjacent pieces!")

                userPlaced = False

                while not userPlaced:
                    newpos1 = input("'2' New Position is : ")

                    # Exit Program
                    if newpos1 == 'exit':
                        sys.exit()
                    newpos1 = int(newpos1)

                    if newpos1 in adjacentLocations(pos1) or only3:

                        if board[newpos1] == 'x':
                            board[pos1] = 'x'
                            board[newpos1] = '2'
                            printBoard(board)

                            if isMill(newpos1, board):
                                userRemoved = False
                                while not userRemoved:
                                    try:
                                        arr = [1, 1, 1, 0]
                                        ans = random.choice(arr)
                                        if ans == 0:
                                            ans = 0.25
                                        else: ans = 0.75 

                                        # printBoard(board)

                                        removepos1 = input("\nA Mill is Formed. Remove Player '1\'s' piece: ")

                                        # Exit Program
                                        if removepos1 == 'exit':
                                            sys.exit()
                                        removepos1 = int(removepos1)

                                        if board[removepos1] == '1' and not isMill(removepos1, board) or allIsMill(board, '1'):
                                            if ans == 0.75:
                                                board[removepos1] = 'x'
                                                userRemoved = True
                                                printBoard(board)
                                                print("Probability of removing Player 1's piece", ans)
                                                print("Remove Successful")
                                            else:
                                                print("Probability of removing Player 1's piece", ans)
                                                print("Cannot Remove. Player '1\'s' turn")
                                                break
                                        else:
                                            print("Invalid Position")
                                            # print("Probability of remomoving Player 1's piece", ans)
                    
                                    except Exception as e:
                                        print(str(e))
                                        print("Error while accepting input")

                            userPlaced = True
                            userMoved = True

                        else:
                            print("Invalid Position")

                    else:
                        print("Only adjacent locations in Stage 2. Try again.")

            except Exception as e:
                print(str(e))

        # printBoard(board)

        if(len(possibleMoves_stage2or3(board, '2')) == 0):
            print("-----------")
            print("    TIE    ")
            print("-----------")
            sys.exit()

        elif numOfPieces(board, '1') < 3:
            print("PLAYER '2' WINS")
            sys.exit()        


if __name__ == "__main__":
    human_vs_human()
