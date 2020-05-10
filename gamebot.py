from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from movement_optimizers import ChainOptimizer, RandomOptimizer, SingleMoveOptimizer

class GameBot:
    def __init__(self, optimizer='montecarlo', n_games=10):
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)
        self.optimization_type = optimizer
        self.n_games = n_games

    def getBestMove(self, game, n_games=10):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = self.getOptimizer(game, type=self.optimization_type)
        bestMove = simulation.getBestMove(n_games=self.n_games)
        return bestMove

    def getOptimizer(self, game, type='chain'):
        if type == 'random':
            return RandomOptimizer(game)
        elif type == 'single':
            return SingleMoveOptimizer(game)
        elif type == 'chain':
            return ChainOptimizer(game)
        else:
            return ValueError('Invalid optimizer type')
