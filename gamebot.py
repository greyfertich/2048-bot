from directions import LEFT, RIGHT, UP, DOWN

class GameBot:
    def __init__(self, gameBoard):
        self.board = gameBoard
        self.scoreboard = [99, 50, 25, 15,
                            5,  7, 10, 12,
                            3,  1,  0,  0,
                            0,  0,  0,  0]

    def getBestMove(self):
        """
        Checks all possible moves and returns the move with highest score
        """
        pass

    def tryMove(self, direction):
        """
        Simulates a move on the game board and returns new score
        """
        return self.getScore(self.board.simulateMove(direction))

    def getScore(self, board):
        """
        Calculates the score of a game board
        """
        return sum(tile*score for tile, score in zip(board, self.scoreboard))
