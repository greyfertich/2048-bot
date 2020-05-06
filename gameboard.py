from directions import LEFT, RIGHT, UP, DOWN

class GameBoard:
    def __init__(self):
        self.grid = [0 for _ in range(16)]

    def getTile(self, index):
        return self.grid[index]

    def setTile(self, index, value):
        self.grid[index] = value

    def simulateMove(self, direction):
        if direction == LEFT:
            sim = self.simulateMoveLeft()
        if direction == RIGHT:
            sim = self.simulateMoveRight()
        if direction == UP:
            sim = self.simulateMoveUp()
        if direction == DOWN:
            sim = self.simulateMoveDown()
        if not self.isGridDifferent(sim):
            return [0] * 16
        return sim

    def isGridDifferent(self, newGrid):
        """
        Compares newGrid to self.grid to see if there are any differences.
        If there are no differences, then the move is invalid.
        """
        return sum(old == new for old, new in zip(self.grid, newGrid)) != len(newGrid)

    def simulateMoveLeft(self):
        return self.makeMove(self.grid)

    def simulateMoveRight(self):
        return self.flipY(self.makeMove(self.flipY(self.grid)))

    def simulateMoveUp(self):
        return self.T(self.makeMove(self.T(self.grid)))

    def simulateMoveDown(self):
        return self.T(self.flipY(self.makeMove(self.flipY(self.T(self.grid)))))

    def makeMove(self, grid):
        newGrid = []
        for i in range(4):
            row = grid[i*4:(i+1)*4]
            newGrid += self.moveRow(row)
        return newGrid

    def flipY(self, grid):
        """
        Flips grid along y axis
        """
        newGrid = []
        for i in range(4):
            newGrid += grid[i*4:(i+1)*4][::-1]
        return newGrid

    def T(self, grid):
        """
        Transposes grid
        """
        newGrid = []
        for i in range(4):
            for c in range(4):
                newGrid.append(grid[i+(c*4)])
        return newGrid

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
