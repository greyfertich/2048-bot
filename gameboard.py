from directions import LEFT, RIGHT, UP, DOWN

class GameBoard:
    def __init__(self, grid):
        self.grid = grid

    def simulateMove(self, direction):
        if direction == LEFT:
            self.simulateMoveLeft()
        if direction == RIGHT:
            self.simulateMoveRight()
        if direction == UP:
            self.simulateMoveUp()
        if direction == DOWN:
            self.simulateMoveDown()

    def simulateMoveLeft(self):
        pass

    def simulateMoveRight(self):
        pass

    def simulateMoveUp(self):
        pass

    def simulateMoveDown(self):
        pass

    def updateBoard(self):
        pass
