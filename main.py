import math
from game import GameBoard
from copy import copy, deepcopy
from blessed import Terminal

# recursive minimax function that traverses the game tree to a given length and 
# determines the optimal outcome
def minimax(board, depth, tergetDepth, maxTurn, alpha=-10000, beta=10000):
    score = board.evaluate()

    if score == 100000000 + 1 or score == -100000000 + 1 or depth == tergetDepth:
        return score
    if board.availableColumns() == []:
        return 0

    if maxTurn:
        best = -1000000000
        for i in board.availableColumns():
            board.place("X", i)
            best = max(best, minimax(board, depth + 1, not maxTurn, alpha, beta))
            board.remove(i)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = 10000000000
        for i in board.availableColumns():
            board.place("O", i)
            best = min(best, minimax(board, depth + 1, not maxTurn, alpha, beta))
            board.remove(i)
            beta = min(best, beta)
            if alpha >= beta:
                break
        return best

# determines the best next move by running the minimax algorithm for each option 
# to find the one that produces the best optimal payoff
def bestMove(board, targetDepth):
    bestVal = -1000
    bestMove = -1
    for i in board.availableColumns():
        board.place("X", i)
        moveVal = minimax(board, 0, targetDepth, False)
        board.remove(i)
        if moveVal > bestVal:
            bestMove = i
            bestVal = moveVal
    return bestMove, bestVal

term = Terminal()
g = GameBoard(6, 7)

# game loop
print(term.home + term.clear + str(g))
while 1:
    # Computer makes its ideal move
    move = bestMove(g, 10)
    print(move)
    g.place("X", move[0])
    # Print the board
    print(
        term.home
        + term.clear
        + str(g)
        .replace("X", term.red + "●" + term.normal)
        .replace("O", term.yellow + "●" + term.normal)
        .replace("_", "○")
    )
    # Check for a computer win
    if g.checkWin("X"):
        print(term.red + term.underline + term.bold + "RED WINS!" + term.normal)
        break
    # Make move based on user input
    move_valid = g.place("O", input("Column: "))
    while move_valid == -1:
        print(
            "enter a valid column number"
            + term.move_up
            + term.move_x(0)
            + term.clear_eol,
            end="",
        )
        move_valid = g.place("O", input("Column: "))
    # Print board
    print(
        term.home
        + term.clear
        + str(g)
        .replace("X", term.red + "●" + term.normal)
        .replace("O", term.yellow + "●" + term.normal)
        .replace("_", "○")
    )
    # Check for a player win
    if g.checkWin("O"):
        print(term.yellow + term.underline + term.bold + "YELLOW WINS!" + term.normal)
        break
