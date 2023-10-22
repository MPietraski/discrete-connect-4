class GameBoard:
    def __init__(self, height, width):
        self.h = height
        self.w = width
        self.board = [ ["_" for i in range(self.w)] for j in range(self.h)]
    
    def __str__(self):
        s = "|"
        for j in range(self.w):
            s += f' {j} |'
        s += "\n"
        for i in range(self.h):
            s += "|"
            for j in range(self.w):
                s += f' {self.board[i][j]} |'
            s += "\n"
        return s[:-1]
    
    def __lt__(self, other):
        return self.getScore() < other.getScore()
    def __gt__(self, other):
        return self.getScore() > other.getScore()
    
    def place(self, symb, row):
        if row > self.w-1:
            print("invalid move")
            return -1
        for i in range(self.h):
            if self.board[i][row] != "_":
                if i == 0:
                    print("invalid move")
                    return -1
                self.board[i-1][row] = symb
                return 1
        self.board[self.h-1][row] = symb
    
    def remove(self, row):
        for i in range(self.h):
            if self.board[i][row] != "_":
                self.board[i][row] = "_"
                return 1
        print("nothing to remove")
        return -1

    def availableColumns(self):
        l = []
        for i, c in enumerate(self.board[0]):
            if c == "_":
                l.append(i)
        return l
    
    def evaluate(self):
        return self.heuristic("X") - self.heuristic("O") + 1

    def heuristic(self, symb):
        score = 0
        for r in range(self.h):
            for c in range(self.w):

                # grid values
                if c > 1 and c < 5:
                    score += 5
                if r > 1 and r < 4:
                    score += 5

                # Lines across rows
                if c+3 < self.w:
                    if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == symb:   # X X X X
                        return 100000000
                    elif self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == symb and self.board[r][c+3] == "_": # X X X _
                        score += 100
                    elif self.board[r][c] == self.board[r][c+1] == symb and self.board[r][c+2] == "_" and self.board[r][c+3] == "_": # X X _ _
                        score += 10
                if c > 0 and c+2 < self.w:
                    if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == symb and self.board[r][c-1] == "_": # _ X X X
                        score += 100
                    elif self.board[r][c] == self.board[r][c+1] == symb and self.board[r][c-1] == "_" and self.board[r][c+2] == "_": # _ X X _
                        score += 10
                    if r > 1:
                        if self.board[r][c] == self.board[r][c+1] == symb and self.board[r][c-2] == "_" and self.board[r][c-1] == "_": # _ _ X X
                            score += 10
                
                # Lines down columns
                if r+3 < self.h:
                    if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == symb:   # X X X X
                        return 100000000
                    if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == symb and self.board[r+3][c] == "_": # X X X _
                        score += 100
                    if self.board[r][c] == self.board[r+1][c] == symb and self.board[r+2][c] == "_" and self.board[r+3][c] == "_": # X X _ _
                        score += 10
                if r > 0 and r+2 < self.h:
                    if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == symb and self.board[r-1][c] == "_": # _ X X X
                        score = 100
                    if self.board[r][c] == self.board[r+1][c] == symb and self.board[r-1][c] == "_" and self.board[r+2][c] == "_": # _ X X _
                        score += 10
                    if c > 1:
                        if self.board[r][c] == self.board[r+1][c] == symb and self.board[r-2][c] == "_" and self.board[r-1][c] == "_": # _ _ X X
                            score += 10
                
                # left right diagonal
                if r+3 < self.h and c+3 < self.w:
                    if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == symb:   # X X X X
                        return 100000000
                    if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == symb and self.board[r+3][c+3] == "_": # X X X _
                        score += 100
                    if self.board[r][c] == self.board[r+1][c+1] == symb and self.board[r+2][c+2] == "_" and self.board[r+3][c+3] == "_": # X X _ _
                        score += 10
                if r > 0 and r+2 < self.h and c > 0 and c+2 < self.w:
                    if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == symb and self.board[r-1][c-1] == "_": # _ X X X
                        score += 100
                    if self.board[r][c] == self.board[r+1][c+1] == symb and self.board[r-1][c-1] == "_" and self.board[r+2][c+2] == "_": # _ X X _
                        score += 10
                    if r> 1 and c > 1:
                        if self.board[r][c] == self.board[r+1][c+1] == symb and self.board[r-2][c-2] == "_" and self.board[r-1][c-1] == "_": # _ _ X X
                            score += 10
                
                # right left diagonal
                if r+3 < self.h and c-3 > 0:
                    if self.board[r][c] == self.board[r+1][c-1] == self.board[r+2][c-2] == self.board[r+3][c-3] == symb:   # X X X X
                        return 100000000
                    if self.board[r][c] == self.board[r+1][c-1] == self.board[r+2][c-2] == symb and self.board[r+3][c-3] == "_": # X X X _
                        score += 100
                    if self.board[r][c] == self.board[r+1][c-1] == symb and self.board[r+2][c-2] == "_" and self.board[r+3][c-3] == "_": # X X _ _
                        score += 10
                if r > 0 and r+2 < self.h and c < self.w-1 and c > 1:
                    if self.board[r][c] == self.board[r+1][c-1] == self.board[r+2][c-2] == symb and self.board[r-1][c+1] == "_": # _ X X X
                        score += 100
                    if self.board[r][c] == self.board[r+1][c-1] == symb and self.board[r-1][c+1] == "_" and self.board[r+2][c-2] == "_": # _ X X _
                        score += 10
                    if r > 1 and c < self.w-2:
                        if self.board[r][c] == self.board[r+1][c-1] == symb and self.board[r-2][c+2] == "_" and self.board[r-1][c+1] == "_": # _ _ X X
                            score += 10
        return score

                


    def checkWin(self, symb):
        curLength = 0
        cutoff = 4
        # Check for horizontal lengths
        for r in range(self.h):
            for c in range(self.w):
                if self.board[r][c] == symb:
                    curLength += 1
                    if curLength >= cutoff:
                        return True
                else:
                    curLength = 0
        # Check for vertical lengths
        for c in range(self.w):
            for r in range(self.h):
                if self.board[r][c] == symb:
                    curLength += 1
                    if curLength >= cutoff:
                        return True
                else:
                    curLength = 0
        # Check for left-right diagonal lengths
        for r in range(self.h):
            for i, c in enumerate(range(self.w)):
                try:
                    if self.board[r+i][c] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return True
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        for c in range(self.w):
            for i, r in enumerate(range(self.h)):
                try:
                    if self.board[r][c+i] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return True
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        # Check for right-left diagonal lengths
        for r in range(self.h):
            for i, c in enumerate(range(self.w)):
                try:
                    if self.board[r-i][c] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return True
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        for c in range(self.w):
            for i, r in enumerate(range(self.h)):
                try:
                    if self.board[r][c-i] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return True
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        return False

    def getMaxLength(self, symb, cutoff=4):
        maxLength = 0
        curLength = 0
        # Check for horizontal lengths
        for r in range(self.h):
            for c in range(self.w):
                if self.board[r][c] == symb:
                    curLength += 1
                    if curLength >= cutoff:
                        return cutoff
                    if curLength > maxLength:
                        maxLength = curLength
                else:
                    curLength = 0
        # Check for vertical lengths
        for c in range(self.w):
            for r in range(self.h):
                if self.board[r][c] == symb:
                    curLength += 1
                    if curLength >= cutoff:
                        return cutoff
                    if curLength > maxLength:
                        maxLength = curLength
                else:
                    curLength = 0
        # Check for left-right diagonal lengths
        for r in range(self.h):
            for i, c in enumerate(range(self.w)):
                try:
                    if self.board[r+i][c] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return cutoff
                        if curLength > maxLength:
                            maxLength = curLength
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        for c in range(self.w):
            for i, r in enumerate(range(self.h)):
                try:
                    if self.board[r][c+i] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return cutoff
                        if curLength > maxLength:
                            maxLength = curLength
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        # Check for right-left diagonal lengths
        for r in range(self.h):
            for i, c in enumerate(range(self.w)):
                try:
                    if self.board[r-i][c] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return cutoff
                        if curLength > maxLength:
                            maxLength = curLength
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        for c in range(self.w):
            for i, r in enumerate(range(self.h)):
                try:
                    if self.board[r][c-i] == symb:
                        curLength += 1
                        if curLength >= cutoff:
                            return cutoff
                        if curLength > maxLength:
                            maxLength = curLength
                    else:
                        curLength = 0
                except:
                    curLength = 0
                    break
        return maxLength

    def getScore(self):
        if self.getMaxLength("X") == 4 and self.getMaxLength("O") != 4:
            return 10
        if self.getMaxLength("X") != 4 and self.getMaxLength("0") == 4:
            return -10
        return self.getMaxLength("X") - self.getMaxLength("O")