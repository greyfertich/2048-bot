import random
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time

class MovementOptimizerInterface:

    def __init__(self, grid):
        self.grid = list(grid)
        self.moves = [LEFT, RIGHT, UP, DOWN]

    def getBestMove(self, **kwargs):
        pass

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

class MonteCarloOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)
        self.scoreboard = [99, 50, 25, 10,
                           50, 30, 20,  10,
                           25, 20,  10,  5,
                           10,  10,  5,  2]
        #self.lookUpTable = self.createLookUpTable()

    def createLookUpTable(self):

        tiles = [0] + [2**i for i in range(1,16)]
        encoded_to_int = {i:n for i,n in enumerate(tiles)}
        int_to_encoded = {n:i for i,n in enumerate(tiles)}

        def encode_row(row):
            encoded_int = 0
            for i,n in enumerate(row):
                encoded_int += int_to_encoded[n] << 12 - (i*4)
            return encoded_int

        count = -1
        table = [0 for _ in range(65536)]
        for i1 in range(16):
            for i2 in range(16):
                for i3 in range(16):
                    for i4 in range(16):
                        count += 1
                        grid_row = [encoded_to_int[i1],encoded_to_int[i2],encoded_to_int[i3],encoded_to_int[i4]]
                        grid_row = self.moveRow(grid_row)
                        table[count] = encode_row(grid_row)
        return table

    def getBestMove(self, n_games=10):
        return self.simulateGame(n_games)

    def simulateGame(self, n_games):
        moveScores = {LEFT: [], RIGHT: [], UP: [], DOWN: []}
        moveCounter = 0
        for i in range(n_games):
            grid = self.grid
            move_counter = 0
            firstMove = -1
            gameOver = False
            depth = 3
            print('starting grid:')
            for i in range(16):
                if i % 4 == 0:
                    print('[ {} {} {} {} ]'.format(grid[i],grid[i+1],grid[i+2],grid[i+3]))
            print()

            while not gameOver and depth >= 0: # While game is not over
                depth -= 1
                move = random.choice(self.moves)
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
                    for move in self.moves:
                        if self.simulateMove(grid, move, checkEnd=True).count(0) != 16:
                            canMoveBeMade = True
                    if not canMoveBeMade:
                        gameOver = True
                print('moved ', KEYMAP[move])
                for i in range(16):
                    if i % 4 == 0:
                        print('[ {} {} {} {} ]'.format(grid[i],grid[i+1],grid[i+2],grid[i+3]))
                print()
            score = sum(tile*score for tile, score in zip(grid, self.scoreboard))
            moveScores[firstMove].append(score)
            print(moveScores)
            time.sleep(2)
        # return best move by score
        return max(moveScores, key=lambda x:(sum(moveScores[x])/len(moveScores[x])) if len(moveScores[x]) > 0 else 0)


class RandomOptimizer(MovementOptimizerInterface):
    def getBestMove(self, **kwargs):
        return random.choice([LEFT, RIGHT, UP, DOWN])

class BruteForceOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)
        self.scoreboard = [99, 50, 25, 10,
                           50, 30, 20,  10,
                           25, 20,  10,  5,
                           10,  10,  5,  2]
        self.n_moves = 3

    def getBestMove(self, **kwargs):
        grid = self.grid
        scoresPerMove = {move:[] for move in self.moves}
        for move in self.moves:
            if self.isMoveValid(grid, move):
                scoresPerMove[move] = self.playAllPossibleGames(self.simulateMove(grid, move), 1, 0)
        move = max(scoresPerMove, key=lambda x:sum(scoresPerMove[x])/len(scoresPerMove[x]) if len(scoresPerMove[x]) > 0 else 0)
        # print('returning move', move)
        # avgs = {KEYMAP[x]: sum(scoresPerMove[x])/len(scoresPerMove[x]) if len(scoresPerMove[x]) > 0 else 0 for x in scoresPerMove}
        # print(avgs)
        return max(scoresPerMove, key=lambda x:sum(scoresPerMove[x])/len(scoresPerMove[x]) if len(scoresPerMove[x]) > 0 else 0)

    def playAllPossibleGames(self, grid, probability, depth):
        scores = []
        if probability < 0.00001:
            return []
        if self.isGameOver(grid):
            # print(' game is ova')
            return [sum(tile*score for tile,score in zip(grid, self.scoreboard))]
        if depth < self.n_moves:
            zeros = [i for i,n in enumerate(grid) if n == 0]
            # print('num zeros: ', zeros)
            for move in self.moves:
                newGrid = self.simulateMove(grid, move, checkEnd=True)
                if newGrid.count(0) < 16:
                    for index in zeros:
                        newGrid[index] = 2
                        scores += self.playAllPossibleGames(newGrid, probability*0.9, depth+1)
                        newGrid[index] = 4
                        scores += self.playAllPossibleGames(newGrid, probability*0.1, depth+1)
                        newGrid[index] = 0
        else:
            scores = [sum(tile*score for tile,score in zip(grid, self.scoreboard))]
        # if len(scores) > 0:
            # print('returning {}'.format(scores))
        return scores

    def isMoveValid(self, grid, move):
        return self.simulateMove(grid, move, checkEnd=True).count(0) < 16

    def isGameOver(self, grid):
        if grid.count(0) == 0:
            count = 0
            for move in self.moves:
                if self.simulateMove(grid, move, checkEnd=True).count(0) == 16:
                    count += 1
            if count == 4:
                return True
        return False
