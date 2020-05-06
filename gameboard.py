from directions import LEFT, RIGHT, UP, DOWN

class GameBoard:
    def __init__(self, grid):
        self.grid = grid
        self.scoreboard = [99, 50, 25, 15,
                            5,  7, 10, 12,
                            3,  1,  0,  0,
                            0,  0,  0,  0]

    def getBestMove(self):
        pass

    def simulateMove(self, direction):
        pass

    def getScore(self):
        pass

    def updateBoard(self):
        pass
