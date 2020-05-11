from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import random

class GameState:
    def __init__(self, grid, score, gameOver):
        self.grid = grid.copy()
        self.score = score
        self.gameOver = gameOver

class Game2048:
    def __init__(self, prev_state=None):
        if prev_state is None:
            self.grid = [0 for i in range(16)]
            while self.grid.count(0) > 14:
                self.placeRandomTile()
            self.score = 0
            self.gameOver = False
        else:
            self.grid = prev_state.grid
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

    def placeRandomTile(self):
        empty_tiles = [i for i,n in enumerate(self.grid) if n == 0]
        tile_value = 2 if random.random() < 0.9 else 4
        if len(empty_tiles) > 0:
            self.grid[random.choice(empty_tiles)] = tile_value

    def placeTile(self, index, value):
        self.grid[index] = value

    def moveAndPlaceRandomTile(self, direction):
        self.move(direction, update_score=True)
        self.placeRandomTile()

    def move(self, direction, update_score=False):
        if direction == LEFT:
            self.moveLeft(update_score=update_score)
        if direction == RIGHT:
            self.moveRight(update_score=update_score)
        if direction == UP:
            self.moveUp(update_score=update_score)
        if direction == DOWN:
            self.moveDown(update_score=update_score)

    def moveIsValid(self, direction):
        current_grid = list(self.grid)
        self.move(direction)
        if current_grid == self.grid:
            return False
        self.grid = current_grid
        return True

    def moveLeft(self, update_score=False):
        self.slideRows(update_score=update_score)

    def moveRight(self, update_score=False):
        self.flip()
        self.slideRows(update_score=update_score)
        self.flip()

    def moveUp(self, update_score=False):
        self.transpose()
        self.slideRows(update_score=update_score)
        self.transpose()

    def moveDown(self, update_score=False):
        self.transpose()
        self.flip()
        self.slideRows(update_score=update_score)
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

    def slideRows(self, update_score=False):
        newGrid = []
        for i in range(4):
            row = self.grid[i*4:(i+1)*4]
            newRow, score_inc = self.slide(row)
            newGrid += newRow
            if update_score:
                self.score += score_inc
        self.grid = newGrid

    def slide(self, row):
        prev = -1
        i = 0
        temp = [0, 0, 0, 0]
        score_inc = 0

        for element in row:
            if element != 0:
                if prev == -1:
                    prev = element
                    temp[i] = element
                    i += 1
                elif prev == element:
                    temp[i-1] = 2*prev
                    score_inc += 2*prev
                    prev = -1
                else:
                    prev = element
                    temp[i] = element
                    i += 1
        return temp, score_inc

    def getEmptyTiles(self):
        return [i for i,n in enumerate(self.grid) if n == 0]

    def printBoard(self):
        for i in range(16):
            if i % 4 == 0:
                print('[ {} {} {} {} ]'.format(self.grid[i],self.grid[i+1],self.grid[i+2],self.grid[i+3]))
        print()
