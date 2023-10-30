from copy import deepcopy
from numpy import inf


# Class to store board state and actions
class GameBoard:
    # initialize board of any size
    def __init__(self, height, width):
        self.h = height
        self.w = width
        self.board = [["_" for i in range(self.w)] for j in range(self.h)]

    # string reppresentation of the current board
    def __str__(self):
        s = "║"
        for j in range(self.w):
            s += f"{j}║"
        s += "\n"
        for i in range(self.h):
            s += "║"
            for j in range(self.w):
                s += f"{self.board[i][j]}║"
            s += "\n"
        return s[:-1]

    # drop a piece, either X or O, in one of the columns
    def place(self, symb, col, do_steps=False, step=0):
        if type(col) is not int:
            if col.isnumeric():
                col = int(col)
            else:
                return -1
        if col > self.w - 1:
            return -1
        for row in range(self.h):
            if self.board[row][col] != "_":
                if row <= 0:
                    return -1
                self.board[row - 1][col] = symb
                return 1
            elif do_steps:
                if row == step:
                    step_board = deepcopy(self)
                    step_board.board[row][col] = symb
                    return (step_board, step + 1)
        self.board[self.h - 1][col] = symb
        return 1

    # remove the top piece of the given column
    def remove(self, row):
        for i in range(self.h):
            if self.board[i][row] != "_":
                self.board[i][row] = "_"
                return 1
        print("nothing to remove")
        return -1

    # returns a list of all columns with space to drop a game piece
    def availableColumns(self):
        l = []
        for i, c in enumerate(self.board[0]):
            if c == "_":
                l.append(i)
        return l

    # calculates the value of the board assuming X is the maximizer and O is the minimizer
    def evaluate(self):
        return self.heuristic("X") - self.heuristic("O")

    # calculates how good a given player is doing in the game, based on the number of pieces
    # they have in a line that has the ability to reach 4
    def heuristic(self, symb):
        score = 0
        for r in range(self.h):
            for c in range(self.w):
                # Lines across rows
                if c + 3 < self.w:
                    if (
                        self.board[r][c]
                        == self.board[r][c + 1]
                        == self.board[r][c + 2]
                        == self.board[r][c + 3]
                        == symb
                    ):  # X X X X
                        return inf
                    elif (
                        self.board[r][c]
                        == self.board[r][c + 1]
                        == self.board[r][c + 2]
                        == symb
                        and self.board[r][c + 3] == "_"
                    ):  # X X X _
                        score += 100
                    elif (
                        self.board[r][c] == self.board[r][c + 1] == symb
                        and self.board[r][c + 2] == "_"
                        and self.board[r][c + 3] == "_"
                    ):  # X X _ _
                        score += 10
                if c > 0 and c + 2 < self.w:
                    if (
                        self.board[r][c]
                        == self.board[r][c + 1]
                        == self.board[r][c + 2]
                        == symb
                        and self.board[r][c - 1] == "_"
                    ):  # _ X X X
                        score += 100
                    elif (
                        self.board[r][c] == self.board[r][c + 1] == symb
                        and self.board[r][c - 1] == "_"
                        and self.board[r][c + 2] == "_"
                    ):  # _ X X _
                        score += 10
                    if r > 1:
                        if (
                            self.board[r][c] == self.board[r][c + 1] == symb
                            and self.board[r][c - 2] == "_"
                            and self.board[r][c - 1] == "_"
                        ):  # _ _ X X
                            score += 10

                # Lines down columns
                if r + 3 < self.h:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c]
                        == self.board[r + 2][c]
                        == self.board[r + 3][c]
                        == symb
                    ):  # X X X X
                        return inf
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c]
                        == self.board[r + 2][c]
                        == symb
                        and self.board[r + 3][c] == "_"
                    ):  # X X X _
                        score += 100
                    if (
                        self.board[r][c] == self.board[r + 1][c] == symb
                        and self.board[r + 2][c] == "_"
                        and self.board[r + 3][c] == "_"
                    ):  # X X _ _
                        score += 10
                if r > 0 and r + 2 < self.h:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c]
                        == self.board[r + 2][c]
                        == symb
                        and self.board[r - 1][c] == "_"
                    ):  # _ X X X
                        score = 100
                    if (
                        self.board[r][c] == self.board[r + 1][c] == symb
                        and self.board[r - 1][c] == "_"
                        and self.board[r + 2][c] == "_"
                    ):  # _ X X _
                        score += 10
                    if c > 1:
                        if (
                            self.board[r][c] == self.board[r + 1][c] == symb
                            and self.board[r - 2][c] == "_"
                            and self.board[r - 1][c] == "_"
                        ):  # _ _ X X
                            score += 10

                # left right diagonal
                if r + 3 < self.h and c + 3 < self.w:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c + 1]
                        == self.board[r + 2][c + 2]
                        == self.board[r + 3][c + 3]
                        == symb
                    ):  # X X X X
                        return inf
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c + 1]
                        == self.board[r + 2][c + 2]
                        == symb
                        and self.board[r + 3][c + 3] == "_"
                    ):  # X X X _
                        score += 100
                    if (
                        self.board[r][c] == self.board[r + 1][c + 1] == symb
                        and self.board[r + 2][c + 2] == "_"
                        and self.board[r + 3][c + 3] == "_"
                    ):  # X X _ _
                        score += 10
                if r > 0 and r + 2 < self.h and c > 0 and c + 2 < self.w:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c + 1]
                        == self.board[r + 2][c + 2]
                        == symb
                        and self.board[r - 1][c - 1] == "_"
                    ):  # _ X X X
                        score += 100
                    if (
                        self.board[r][c] == self.board[r + 1][c + 1] == symb
                        and self.board[r - 1][c - 1] == "_"
                        and self.board[r + 2][c + 2] == "_"
                    ):  # _ X X _
                        score += 10
                    if r > 1 and c > 1:
                        if (
                            self.board[r][c] == self.board[r + 1][c + 1] == symb
                            and self.board[r - 2][c - 2] == "_"
                            and self.board[r - 1][c - 1] == "_"
                        ):  # _ _ X X
                            score += 10

                # right left diagonal
                if r + 3 < self.h and c - 3 > 0:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c - 1]
                        == self.board[r + 2][c - 2]
                        == self.board[r + 3][c - 3]
                        == symb
                    ):  # X X X X
                        return inf
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c - 1]
                        == self.board[r + 2][c - 2]
                        == symb
                        and self.board[r + 3][c - 3] == "_"
                    ):  # X X X _
                        score += 100
                    if (
                        self.board[r][c] == self.board[r + 1][c - 1] == symb
                        and self.board[r + 2][c - 2] == "_"
                        and self.board[r + 3][c - 3] == "_"
                    ):  # X X _ _
                        score += 10
                if r > 0 and r + 2 < self.h and c < self.w - 1 and c > 1:
                    if (
                        self.board[r][c]
                        == self.board[r + 1][c - 1]
                        == self.board[r + 2][c - 2]
                        == symb
                        and self.board[r - 1][c + 1] == "_"
                    ):  # _ X X X
                        score += 100
                    if (
                        self.board[r][c] == self.board[r + 1][c - 1] == symb
                        and self.board[r - 1][c + 1] == "_"
                        and self.board[r + 2][c - 2] == "_"
                    ):  # _ X X _
                        score += 10
                    if r > 1 and c < self.w - 2:
                        if (
                            self.board[r][c] == self.board[r + 1][c - 1] == symb
                            and self.board[r - 2][c + 2] == "_"
                            and self.board[r - 1][c + 1] == "_"
                        ):  # _ _ X X
                            score += 10
        return score
