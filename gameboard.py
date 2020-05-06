from directions import LEFT, RIGHT, UP, DOWN

class GameBoard:
    def __init__(self, grid):
        self.grid = grid

    def simulateMove(self, direction):
        if direction == LEFT:
            self.simulateMoveLeft()
        if direction == RIGHT:
            self.simulateMoveRight()
        if direction == UP:
            self.simulateMoveUp()
        if direction == DOWN:
            self.simulateMoveDown()
        return self.grid

    def simulateMoveLeft(self):
        self.makeMove()

    def simulateMoveRight(self):
        self.flipHorizontally()
        self.makeMove()
        self.flipHorizontally()

    def simulateMoveUp(self):
        self.transpose()
        self.makeMove()
        self.transpose()

    def simulateMoveDown(self):
        self.transpose()
        self.flipHorizontally()
        self.makeMove()
        self.flipHorizontally()
        self.transpose()

    def makeMove(self):
        newGrid = []
        for i in range(4):
            row = self.grid[i*4:(i+1)*4]
            newGrid.append(self.moveRow(row))
        self.grid = newGrid

    def flipHorizontally(self):
        newGrid = []
        for i in range(4):
            newGrid += self.grid[i*4,(i+1)*4][::-1]
        self.grid = newGrid

    def transpose(self):
        newGrid = []
        for i in range(4):
            for c in range(4):
                newGrid.append(self.grid[i+(c*4)])
        self.grid = newGrid

    def moveRow(self, row):
        prev = -1
        i = 0
        temp = [0, 0, 0, 0]

        for element in row:

            if element != 0:
                if prev == -1:
                    prev = element
                    temp[i] = element
                    i += 1
                elif prev == element:
                    temp[i - 1] = 2 * prev
                    prev = -1
                else:
                    prev = element
                    temp[i] = element
                    i += 1

        return temp

    def update(self):
        pass
