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


class SingleMoveOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)

    def getBestMove(self, **kwargs):
        state = GameState(self.game.getGrid(), self.game.getScore(), self.game.isGameOver())
        scores = {move:0 for move in self.moves}
        for move in self.moves:
            newGame = Game2048(prev_state=state)
            if newGame.moveIsValid(move):
                newGame.move(move)
                scores[move] = self.evaluate(newGame)
        return max(scores, key=lambda x:scores[x])


class RandomOptimizer(MovementOptimizerInterface):
    def getBestMove(self, **kwargs):
        return random.choice([LEFT, RIGHT, UP, DOWN])


class ExpectimaxOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)
        self.funcCalls = 0

    def getBestMove(self, depth=2, **kwargs):
        #print('cur')
        #self.game.printBoard()
        move, score = self.maxValue(self.game, depth=0, max_depth=depth)
        #time.sleep(10)
        return move

    def maxValue(self, game, depth, max_depth):
        bestScore = -1
        bestMove = 0
        state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
        for move in self.moves:
            newGame = Game2048(prev_state=state)
            if newGame.moveIsValid(move):
                newGame.move(move)
                #print('Trying move', KEYMAP[move])
                #newGame.printBoard()
                value = self.expectedValue(newGame, depth, max_depth)
                #print('{}: {}'.format(KEYMAP[move], value))
                if value > bestScore:
                    bestScore = value
                    bestMove = move
        return bestMove, bestScore

    def expectedValue(self, game, depth, max_depth):
        state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
        emptyTiles = game.getEmptyTiles()
        n_empty = len(emptyTiles)
        score = 0
        #print('In expected looking at board: ')
        #print(game.printBoard())
        #print('EXPECTED')
        for tile in emptyTiles:
            for tileValue, prob in zip([2,4],[0.9,0.1]):
                newGame = Game2048(prev_state=state)
                newGame.placeTile(tile, tileValue)
                #print('Score:', self.evaluate(newGame))
                #newGame.printBoard()
                if depth < max_depth:
                    move, value = self.maxValue(newGame, depth+1, max_depth)
                else:
                    value = self.evaluate(newGame)
                #print('value: {}, prob: {}'.format(value, prob/n_empty))
                #print('score update: {}'.format((prob/n_empty)*value))
                score += (prob/n_empty) * value
        #print('returning score: {}'.format(score))
        return score

    # def value(self, game, depth, max_depth):
    #     state = GameState(game.getGrid(), game.getScore(), game.isGameOver())
    #     return self.maxValue(game, depth, max_depth)



class ChainOptimizer(MovementOptimizerInterface):
    def __init__(self, game):
        super().__init__(game)

    def getBestMove(self, depth=5, **kwargs):
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
