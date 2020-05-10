import random
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time
from game import Game2048, GameState

class MovementOptimizerInterface:

    def __init__(self, game):
        self.game = game
        self.moves = [LEFT, RIGHT, UP, DOWN]

    def getBestMove(self, **kwargs):
        pass


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


class RandomOptimizer(MovementOptimizerInterface):
    def getBestMove(self, **kwargs):
        return random.choice([LEFT, RIGHT, UP, DOWN])
        

class ExpectiMiniMaxOptimizer(MovementOptimizerInterface):
    def __init__(self, grid):
        super().__init__(grid)

    def getBestMove(self, **kwargs):
        pass

class ChainOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)
        row1 = [1/(2**i) for i in range(4)]
        row2 = [1/(2**i) for i in range(4,8)][::-1]
        row3 = [1/(2**i) for i in range(8,12)]
        row4 = [1/(2**i) for i in range(12,16)][::-1]
        self.scoreboard = row1 + row2 + row3 + row4


    def getBestMove(self, depth=5, **kwargs):
        move, score = self.nextMoveRecur(self.game, depth, depth)
        return move
    def nextMoveRecur(self, game, depth, max_depth, base=0.9):
        bestScore = -1
        bestMove = 0
        for move in self.moves:
            state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
            newGame = Game2048(prev_state=state)
            if (newGame.moveIsValid(move)):
                newGame.move(move)
                score = self.evaluate(newGame)
                if depth != 0:
                    my_move, my_score = self.nextMoveRecur(newGame, depth-1, max_depth)
                    score += my_score*pow(base,max_depth-depth+1)
                if score > bestScore:
                    bestMove = move
                    bestScore = score
        return (bestMove, bestScore)

    def evaluate(self, game):
        return sum(tile*score for tile,score in zip(game.getGrid(), self.scoreboard))
