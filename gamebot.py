from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from movement_optimizers import ChainOptimizer, MonteCarloOptimizer, RandomOptimizer, BruteForceOptimizer, SingleMoveOptimizer

class GameBot:
    def __init__(self, optimizer='montecarlo', n_games=10):
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)
        self.optimization_type = optimizer
        self.n_games = n_games

    def getBestMove(self, board, n_games=10):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = self.getOptimizer(board.getGrid(), type=self.optimization_type)
        # for i in range(16):
        #     if i % 4 == 0:
        #         g = board.getGrid()
        #         print('[ {} {} {} {} ]'.format(g[i],g[i+1],g[i+2],g[i+3]))
        # print()
        bestMove = simulation.getBestMove(n_games=self.n_games)
        return bestMove

    def getOptimizer(self, grid, type='montecarlo'):
        if type == 'montecarlo':
            return MonteCarloOptimizer(grid)
        elif type == 'random':
            return RandomOptimizer(grid)
        elif type == 'bruteforce':
            return BruteForceOptimizer(grid)
        elif type == 'single':
            return SingleMoveOptimizer(grid)
        elif type == 'chain':
            return ChainOptimizer(grid)
        else:
            return ValueError('Invalid optimizer type')
