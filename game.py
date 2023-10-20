class GameBoard:
    def __init__(self, height, width):
        self.h = height
        self.w = width
        self.board = [ ["_" for i in range(self.w)] for j in range(self.h)]
    
    def __str__(self):
        s = ""
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
        if self.checkWin("X"):
            return 10
        if self.checkWin("O"):
            return -10
        return 0

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