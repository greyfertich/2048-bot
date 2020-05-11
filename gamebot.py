from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from movement_optimizers import ExpectimaxOptimizer, ChainOptimizer

class GameBot:
    def __init__(self, optimizer='montecarlo', depth=1):
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)
        self.optimization_type = optimizer
        self.depth = depth

    def getBestMove(self, game):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = self.getOptimizer(game, type=self.optimization_type)
        bestMove = simulation.getBestMove(depth=self.depth)
        return bestMove

    def getOptimizer(self, game, type='expectimax'):
        if type == 'chain':
            return ChainOptimizer(game)
        elif type == 'expectimax':
            return ExpectimaxOptimizer(game)
        else:
            return ValueError('Invalid optimizer type')
