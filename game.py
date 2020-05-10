from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import random

class GameState:
    def __init__(self, grid, score, gameOver):
        self.grid = grid
        self.score = score
        self.gameOver = gameOver

class Game2048:
    def __init__(self, prev_state=None):
        if prev_state is None:
            self.initializeGame()
        else:
            self.grid = list(prev_state.grid)
            self.score = prev_state.score
            self.gameOver = prev_state.gameOver

    def getScore(self):
        return self.score

    def getGrid(self):
        return self.grid

    def isGameOver(self):
        gameOver = True
        for direction in [LEFT, RIGHT, UP, DOWN]:
            if self.moveIsValid(direction):
                gameOver = False
        self.gameOver = gameOver
        return self.gameOver

    def initializeGame(self):
        self.grid = [0 for i in range(16)]
        while self.grid.count(0) > 14:
            self.placeRandomTile()
        self.score = 0
        self.gameOver = False

    def placeRandomTile(self):
        empty_tiles = [i for i,n in enumerate(self.grid) if n == 0]
        tile_value = 2 if random.random() < 0.9 else 4
        if len(empty_tiles) > 0:
            self.grid[random.choice(empty_tiles)] = tile_value

    def moveAndPlaceRandomTile(self, direction):
        self.move(direction)
        self.placeRandomTile()

    def move(self, direction):
        if direction == LEFT:
            self.moveLeft()
        if direction == RIGHT:
            self.moveRight()
        if direction == UP:
            self.moveUp()
        if direction == DOWN:
            self.moveDown()

    def moveIsValid(self, direction):
        current_grid = list(self.grid)
        self.move(direction)
        if current_grid == self.grid:
            return False
        self.grid = current_grid
        return True

    def moveLeft(self):
        self.slideRows()

    def moveRight(self):
        self.flip()
        self.slideRows()
        self.flip()

    def moveUp(self):
        self.transpose()
        self.slideRows()
        self.transpose()

    def moveDown(self):
        self.transpose()
        self.flip()
        self.slideRows()
        self.flip()
        self.transpose()

    def transpose(self):
        """
        Transposes grid
        """
        self.grid = [self.grid[i+(c*4)] for i in range(4) for c in range(4)]

    def flip(self):
        """
        Flips grid horizontally
        """
        newGrid = []
        for i in range(4):
            newGrid += self.grid[i*4:(i+1)*4][::-1]
        self.grid = newGrid

    def slideRows(self):
        newGrid = []
        for i in range(4):
            row = self.grid[i*4:(i+1)*4]
            newGrid += self.slide(row)
        self.grid = newGrid

    def slide(self, row):
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
                    temp[i-1] = 2*prev
                    self.score += 2*prev
                    prev = -1
                else:
                    prev = element
                    temp[i] = element
                    i += 1
        return temp

    def printBoard(self):
        for i in range(16):
            if i % 4 == 0:
                print('[ {} {} {} {} ]'.format(self.grid[i],self.grid[i+1],self.grid[i+2],self.grid[i+3]))
        print()
