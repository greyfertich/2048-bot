from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from movement_optimizers import MonteCarloOptimizer, RandomOptimizer, BruteForceOptimizer

class GameBot:
    def __init__(self, optimizer='montecarlo'):
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)
        self.optimization_type = optimizer

    def getBestMove(self, board):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = self.getOptimizer(board.getGrid(), type=self.optimization_type)
        bestMove = simulation.getBestMove(n_games=10)
        return bestMove

    def getOptimizer(self, grid, type='montecarlo'):
        if type == 'montecarlo':
            return MonteCarloOptimizer(grid)
        elif type == 'random':
            return RandomOptimizer(grid)
        elif type == 'bruteforce':
            return BruteForceOptimizer(grid)
        else:
            return ValueError('Invalid optimizer type')
