# Based on code from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction
import math
from game import GameBoard
from copy import copy, deepcopy

counter = 0

def minimax2(board, depth, tergetDepth, maxTurn, alpha=-10000, beta=10000):
    score = board.evaluate()

    if score == 100000000+1 or score == -100000000+1 or depth == tergetDepth:
        return score
    if board.availableColumns() == []:
        return 0
    
    if maxTurn:
        best = -1000000000
        for i in board.availableColumns():
            board.place("X",i)
            best = max(best, minimax2(board, depth+1, not maxTurn, alpha, beta))
            board.remove(i)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = 10000000000
        for i in board.availableColumns():
            board.place("O",i)
            best = min(best,minimax2(board, depth+1, not maxTurn, alpha, beta))
            board.remove(i)
            beta = min(best, beta)
            if alpha >= beta:
                break
        return best

def bestMove(board, targetDepth):
    bestVal = -1000
    bestMove = -1

    for i in board.availableColumns():
        board.place("X",i)
        moveVal = minimax2(board, 0, targetDepth, False)
        board.remove(i)
        if moveVal > bestVal:
            bestMove = i
            bestVal = moveVal
    return bestMove, bestVal

def minimax(depth, targetDepth, column, board, maxTurn):
    '''
    Recursive minimax function of a game tree with n branches from each internal 
    node
   
    Parameters:
        depth: the current depth into te tree, starting at 0 for the root
        targetDepth: the depth to go to to count wins
        column: the column that was just dropped into
        board: the board before the next move
        maxTurn: True if it is the maximizer's turn, False if it is not
    Returns:
        The payoff at the end of an optimized game
    '''
    global counter
    counter += 1
    # print(counter,depth,column)
    if column >= 0:
        if maxTurn: 
            symb = "O"
        else:
            symb = "X"
        board.place(symb, column)
    
    if (depth == targetDepth):
        return board

    nextLevel = [minimax(depth+1, targetDepth, i, deepcopy(board), not(maxTurn)) for i in board.avaliableColumns()]

    if(maxTurn):
        return max(nextLevel)
    else:
        return min(nextLevel)

g = GameBoard(6, 7)
# g.place("X",5)
# g.place("O",5)
# g.place("O",5)
# g.place("O",5)

# g.board[0][2] = "-"
# g.board[0][3] = "-"
# g.board[0][4] = "-"
# g.board[0][5] = "-"
# g.board[0][6] = "-"

# for i in [2,4,6]:
#     g.place("X",i)
#     g.place("X",i)
#     g.place("O",i)
#     g.place("O",i)
#     g.place("X",i)
#     g.place("X",i)
# for i in [3,5]:
#     g.place("O",i)
#     g.place("O",i)
#     g.place("X",i)
#     g.place("X",i)
#     g.place("O",i)
#     g.place("O",i)

print(g)
while 1:
    move = bestMove(g, 10)
    print(move)
    g.place("X",move[0])
    print(g)
    if g.checkWin("X"):
        print("X WINS")
        break
    col = input("Column: ")
    while not col.isnumeric():
        col = input("Column: ")
    g.place("O", int(col))
    print(g)
    if g.checkWin("O"):
        print("O WINS")
        break
# r = minimax(0, 3, -1, g, True)
# print(r)
