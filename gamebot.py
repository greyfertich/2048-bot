from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from montecarlo import MonteCarloSimulation

class GameBot:
    def __init__(self, gameClient):
        self.client = gameClient
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)

    def getBestMove(self):
        """
        Checks all possible moves and returns the move with highest score
        """
        simulation = MonteCarloSimulation(self.client.getBoard().getGrid())
        bestMove = simulation.simulateGame(n_games=10)
        self.client.updateScore(bestMove)
        return bestMove

    def tryMove(self, direction):
        """
        Simulates a move on the game board and returns new score
        """
        return self.getScore(self.client.getBoard().simulateMove(direction))

    def getScore(self, board):
        """
        Calculates the score of a game board
        """
        return sum(tile*score for tile, score in zip(board, self.scoreboard))

    def updateBoard(self):
        self.client.readBoardFromWindow()
