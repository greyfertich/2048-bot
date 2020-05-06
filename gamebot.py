from directions import LEFT, RIGHT, UP, DOWN, KEYMAP

class GameBot:
    def __init__(self, gameClient):
        self.client = gameClient
        self.scoreboard = [99, 50, 25, 15,
                            5,  7, 10, 12,
                            3,  1,  0,  0,
                            0,  0,  0,  0]
        self.possibleMoves = (LEFT, RIGHT, UP, DOWN)

    def getBestMove(self):
        """
        Checks all possible moves and returns the move with highest score
        """
        m = 0
        for move in self.possibleMoves:
            m = max(m,self.tryMove(move))
        return m
        #return max([(move, self.tryMove(move)) for move in self.possibleMoves], key=lambda x: x[1])[0]

    def tryMove(self, direction):
        """
        Simulates a move on the game board and returns new score
        """
        newGrid = self.client.getBoard().simulateMove(direction)
        print(KEYMAP[direction])
        self.client.printGrid(newGrid)
        return self.getScore(self.client.getBoard().simulateMove(direction))

    def getScore(self, board):
        """
        Calculates the score of a game board
        """
        return sum(tile*score for tile, score in zip(board, self.scoreboard))

    def updateBoard(self):
        self.client.readBoardFromWindow()
