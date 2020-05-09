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

    def isMoveValid(self, grid, move):
        return self.simulateMove(grid, move, checkEnd=True).count(0) < 16

class SingleMoveOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)
        self.scoreboard = [99, 50, 25, 10,
                           50, 30, 20,  0,
                           25, 20,  0,  0,
                           10,  0,  0,  0]

    def getBestMove(self, **kwargs):
        grid = self.grid
        scores = {move:0 for move in self.moves}
        for move in self.moves:
            if self.isMoveValid(grid, move):
                scores[move] = self.score(self.simulateMove(grid, move))
        return max(scores, key=lambda x:scores[x])

    def score(self, grid):
        return sum([tile*score for tile,score in zip(grid, self.scoreboard)])

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
        return self.getMaxMove(n_games)

    def getMaxMove(self, n_games):
        mins = {}
        b = False
        for move in self.moves:
            if self.isMoveValid(self.grid, move):
                mins[move] = self.simulateGame(n_games)
                b = True
        # print('mins:', mins)
        # print(b)
        return max(mins, key=lambda x:mins[x])


    def simulateGame(self, n_games):
        moveScores = {move:0 for move in self.moves}
        moveCounter = 0
        for i in range(n_games):
            grid = self.grid
            move_counter = 0
            firstMove = -1
            gameOver = False
            depth = 3

            while not gameOver and depth >= 0: # While game is not over
                #depth -= 1
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
                        if self.isMoveValid(grid, move):
                            canMoveBeMade = True
                    if not canMoveBeMade:
                        gameOver = True
            score = sum(tile*score for tile, score in zip(grid, self.scoreboard))
            moveScores[firstMove] = min(score, moveScores[firstMove]) if moveScores[firstMove] > 0 else score
        # return best move by score
        return min(moveScores.values())


class RandomOptimizer(MovementOptimizerInterface):
    def getBestMove(self, **kwargs):
        return random.choice([LEFT, RIGHT, UP, DOWN])

class BruteForceOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)
        self.scoreboard = [99, 50, 25, 10,
                           0,  0,  3,  5,
                           0,  0,  0,  0,
                            0,  0,  0,  0]
        self.n_moves = 1
        self.move_sequence = []

    def getBestMove(self, **kwargs):
        if len(self.move_sequence) > 0:
            return self.move_sequence.pop(0)
        grid = self.grid
        self.move_sequence = []
        highest_score = 0

        for move in self.moves:
            if self.isMoveValid(grid, move):
                seq, score = self.playAllPossibleGames(self.simulateMove(grid, move), 1, 0)
                print(score, seq)
                if score > highest_score:
                    highest_score = score
                    self.move_sequence = [move] + seq
        return self.move_sequence.pop(0)

    def playAllPossibleGames(self, grid, probability, depth):
        scores = []
        if probability < 0.00001:
            return []
        if self.isGameOver(grid):
            return [sum(tile*score for tile,score in zip(grid, self.scoreboard))]
        if depth < self.n_moves:
            zeros = [i for i,n in enumerate(grid) if n == 0]
            endScore, endSeq = 0, []
            for move in self.moves:
                curSeq = [move]
                curScore = 0
                newGrid = self.simulateMove(grid, move, checkEnd=True)
                if newGrid.count(0) < 16:
                    for index in zeros:
                        newGrid[index] = 2
                        seq, score = self.playAllPossibleGames(newGrid, probability*0.9, depth+1)
                        if score > curScore:
                            curScore = score
                            curSeq += seq
                        newGrid[index] = 4
                        seq, score = self.playAllPossibleGames(newGrid, probability*0.1, depth+1)
                        if score > curScore:
                            curScore = score
                            curSeq += seq
                        newGrid[index] = 0
                if curScore > endScore:
                    endScore = curScore
                    endSeq = curSeq
            return endSeq, curScore
        else:
            score = sum(tile*score for tile, score in zip(grid, self.scoreboard))
            seq = []
        return seq, score

    def isGameOver(self, grid):
        if grid.count(0) == 0:
            count = 0
            for move in self.moves:
                if self.simulateMove(grid, move, checkEnd=True).count(0) == 16:
                    count += 1
            if count == 4:
                return True
        return False

class ExpectiMiniMaxOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)

    def getBestMove(self, **kwargs):
        pass

class ChainOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)
        row1 = [1/(2**i) for i in range(4)]
        row2 = [1/(2**i) for i in range(4,8)][::-1]
        row3 = [1/(2**i) for i in range(8,12)]
        row4 = [1/(2**i) for i in range(12,16)][::-1]
        self.scoreboard = row1 + row2 + row3 + row4


    def getBestMove(self, depth=3, **kwargs):
        move, score = self.nextMoveRecur(self.grid, depth, depth)
        return move
    def nextMoveRecur(self, grid, depth, max_depth, base=0.9):
        bestScore = -1
        bestMove = 0
        for move in self.moves:
            newGrid = list(grid)
            if (self.isMoveValid(newGrid, move)):
                newGrid = self.simulateMove(newGrid, move)
                score = self.evaluate(newGrid)
                if depth != 0:
                    my_move, my_score = self.nextMoveRecur(newGrid, depth-1, max_depth)
                    score += my_score*pow(base,max_depth-depth+1)
                if score > bestScore:
                    bestMove = move
                    bestScore = score
        #print(self.isMoveValid(newGrid,bestMove))
        return (bestMove, bestScore)
    def evaluate(self, grid):
        return sum(tile*score for tile,score in zip(grid, self.scoreboard))
