import random
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time

class MovementOptimizerInterface:

    def __init__(self, grid):
        pass

    def getBestMove(self, **kwargs):
        pass

class MonteCarloOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        self.grid = list(grid)
        self.scoreboard = [99, 50, 25, 10,
                           50, 30, 20,  10,
                           25, 20,  10,  5,
                           10,  10,  5,  2]


    def getBestMove(self, n_games=100):
        return self.simulateGame(n_games)

    def simulateGame(self, n_games):
        moves = [LEFT, RIGHT, UP, DOWN]
        moveScores = {LEFT: [], RIGHT: [], UP: [], DOWN: []}
        moveCounter = 0
        for i in range(n_games):
            grid = self.grid
            move_counter = 0
            firstMove = -1
            gameOver = False
            while not gameOver: # While game is not over
                move = random.choice(moves)
                if move_counter == 0:
                    firstMove = move
                move_counter += 1
                grid = self.simulateMove(grid, move)
                self.simulateRandomTilePlacement(grid)
                if grid.count(0) == 16:
                    gameOver = True
                if grid.count(0) == 0:
                    # check to see if any possible moves can be made
                    canMoveBeMade = False
                    for move in moves:
                        if self.simulateMove(grid, move, checkEnd=True).count(0) != 16:
                            canMoveBeMade = True
                    if not canMoveBeMade:
                        gameOver = True
            score = sum(tile*score for tile, score in zip(grid, self.scoreboard))
            moveScores[firstMove].append(score)
        # return best move by score
        return max(moveScores, key=lambda x:(sum(moveScores[x])/len(moveScores[x])) if len(moveScores[x]) > 0 else 0)

    def simulateMove(self, grid, direction, checkEnd=False):
        if direction == LEFT:
            sim = self.simulateMoveLeft(grid)
        if direction == RIGHT:
            sim = self.simulateMoveRight(grid)
        if direction == UP:
            sim = self.simulateMoveUp(grid)
        if direction == DOWN:
            sim = self.simulateMoveDown(grid)
        if checkEnd and not self.isGridDifferent(grid, sim):
            return [0] * 16
        return sim

    def isGridDifferent(self, grid, newGrid):
        """
        Compares newGrid to self.grid to see if there are any differences.
        If there are no differences, then the move is invalid.
        """
        return sum(old == new for old, new in zip(grid, newGrid)) != len(newGrid)

    def simulateMoveLeft(self, grid):
        return self.makeMove(grid)

    def simulateMoveRight(self, grid):
        return self.flipY(self.makeMove(self.flipY(grid)))

    def simulateMoveUp(self, grid):
        return self.T(self.makeMove(self.T(grid)))

    def simulateMoveDown(self, grid):
        return self.T(self.flipY(self.makeMove(self.flipY(self.T(grid)))))

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
                    temp[i-1] = 2*prev
                    prev = -1
                else:
                    prev = element
                    temp[i] = element
                    i += 1
        return temp

    def simulateRandomTilePlacement(self, grid):
        emptyTiles = [i for i,n in enumerate(grid) if n == 0]
        if len(emptyTiles) > 0:
            randomTileValue = 2 if random.random() < 0.9 else 4
            grid[random.choice(emptyTiles)] = randomTileValue


class RandomOptimizer(MovementOptimizerInterface):
    def getBestMove(self, **kwargs):
        return random.choice([LEFT, RIGHT, UP, DOWN])
