from directions import LEFT, RIGHT, UP, DOWN, KEYMAP

class GameBot:
    def __init__(self, gameClient):
        self.client = gameClient
        self.scoreboard = [99, 50, 25, 10,
                           50, 30, 20,  10,
                           25, 20,  10,  5,
                           10,  10,  5,  2]
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)

    def getBestMove(self):
        """
        Checks all possible moves and returns the move with highest score
        """
        bestMove = max([(move, self.tryMove(move)) for move in self.possibleMoves], key=lambda x: x[1])[0]
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
