from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from montecarlo import MonteCarloSimulation

class GameBot:
    def __init__(self):
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)

    def getBestMove(self, board):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = MonteCarloSimulation(board.getGrid())
        bestMove = simulation.simulateGame(n_games=10)
        return bestMove
