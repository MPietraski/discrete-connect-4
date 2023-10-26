from game import GameBoard
import time
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


def prettyPrintBoard(board):
    print(
        term.home
        + str(board)
        .replace("X", term.red + "●" + term.normal)
        .replace("O", term.yellow + "●" + term.normal)
        .replace("_", "○"),
        end="",
        flush=True,
    )


def printXY(x, y, char):
    print(
        term.move_xy(x, y) + char + term.move_xy(x, y),
        end="",
        flush=True,
    )


def printCursor():
    printXY(2 * col + 1, 0, term.yellow + "●" + term.normal)
    print(term.move_xy(0, 7), end="", flush=True)


def eraseCursor():
    printXY(2 * col + 1, 0, str(col))


def animatedPlace(board, symb, col):
    val = (board, 0)
    while type(val) is not int:
        time.sleep(0.1)
        val = board.place(symb, col, True, val[1])
        if type(val) is int:
            break
        prettyPrintBoard(val[0])
        printCursor()


term = Terminal()
g = GameBoard(6, 7)

col = 0  # user selected column

# game loop
print(term.home + term.clear, end="", flush=True)
prettyPrintBoard(g)
printCursor()
print(
    "Use the arrow keys to select a column.\nPress Enter, Space, or ↓ to drop your piece."
)
while 1:
    # Computer makes its ideal move
    move = bestMove(g, 10)
    # print(move)
    animatedPlace(g, "X", move[0])
    # Print the board
    prettyPrintBoard(g)
    printCursor()
    # Check for a computer win
    if g.checkWin("X"):
        print(term.clear)
        prettyPrintBoard(g)
        print("\n" + term.red + term.underline + term.bold + "RED WINS!" + term.normal)
        break
    # Make move based on user input
    with term.cbreak():
        # if prev selected column unavailable, move to next
        while col not in g.availableColumns():
            eraseCursor()
            col += 1
            if col > 6:  # wrap to left if all cols to right are unavailable
                col = 0
            printCursor()
        val = ""
        next_col = False
        while val != " ":
            val = term.inkey(timeout=3)
            if val.is_sequence:
                if val.name in ["KEY_ENTER", "KEY_DOWN"]:
                    break
                if val.name == "KEY_LEFT":
                    # get next available selection to the left
                    next_col = next(
                        (c for c in g.availableColumns()[::-1] if c < col), False
                    )
                if val.name == "KEY_RIGHT":
                    # get next available selection to the right
                    next_col = next((c for c in g.availableColumns() if c > col), False)
                if next_col is not False:
                    eraseCursor()
                    col = next_col
                    printCursor()
        move_valid = animatedPlace(g, "O", col)
    # Print board
    prettyPrintBoard(g)
    printCursor()
    # Check for a player win
    if g.checkWin("O"):
        print(term.clear)
        prettyPrintBoard(g)
        print(
            "\n"
            + term.yellow
            + term.underline
            + term.bold
            + "YELLOW WINS!"
            + term.normal
        )
        break
