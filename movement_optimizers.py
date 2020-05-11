import random
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time
from game import Game2048, GameState

class MovementOptimizerInterface:

    def __init__(self, game):
        self.game = game
        self.moves = [LEFT, RIGHT, UP, DOWN]
        row1 = [1/(2**i) for i in range(4)]
        row2 = [1/(2**i) for i in range(4,8)][::-1]
        row3 = [1/(2**i) for i in range(8,12)]
        row4 = [1/(2**i) for i in range(12,16)][::-1]
        self.scoreboard = row1 + row2 + row3 + row4

    def getBestMove(self, **kwargs):
        pass

    def evaluate(self, game):
        return sum(tile*score for tile,score in zip(game.getGrid(), self.scoreboard))


class ExpectimaxOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)
        self.funcCalls = 0

    def getBestMove(self, depth=2):
        move, score = self.maxValue(self.game, depth=0, max_depth=depth)
        return move

    def maxValue(self, game, depth, max_depth):
        bestScore = -1
        bestMove = 0
        state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
        for move in self.moves:
            newGame = Game2048(prev_state=state)
            if newGame.moveIsValid(move):
                newGame.move(move)
                value = self.expectedValue(newGame, depth, max_depth)
                if value > bestScore:
                    bestScore = value
                    bestMove = move
        return bestMove, bestScore

    def expectedValue(self, game, depth, max_depth):
        state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
        emptyTiles = game.getEmptyTiles()
        n_empty = len(emptyTiles)
        score = 0
        for tile in emptyTiles:
            for tileValue, prob in zip([2,4],[0.9,0.1]):
                newGame = Game2048(prev_state=state)
                newGame.placeTile(tile, tileValue)
                if depth < max_depth:
                    move, value = self.maxValue(newGame, depth+1, max_depth)
                else:
                    value = self.evaluate(newGame)
                score += (prob/n_empty) * value
        return score


class ChainOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)

    def getBestMove(self, depth=5):
        move, score = self.nextMoveRecur(self.game, 0, depth)
        return move

    def nextMoveRecur(self, game, depth, max_depth, base=0.9):
        bestScore = -1
        bestMove = 0
        state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
        for move in self.moves:
            newGame = Game2048(prev_state=state)
            if (newGame.moveIsValid(move)):
                newGame.move(move)
                score = self.evaluate(newGame)
                if depth <= max_depth:
                    my_move, my_score = self.nextMoveRecur(newGame, depth+1, max_depth)
                    score += my_score*pow(base, depth+1)
                if score > bestScore:
                    bestMove = move
                    bestScore = score
        return (bestMove, bestScore)
