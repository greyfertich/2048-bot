from gamebot import GameBot
from gameclient import BrowserClient, LocalClient
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time

class GameController:

    def __init__(self, gameplayMode='local', optimizer='montecarlo', n_games=10):
        self.client = self.getGameClient(gameplayMode)
        self.bot = GameBot(optimizer, n_games=n_games)

    def getGameClient(self, gameplayMode):
        if gameplayMode == 'browser':
            return BrowserClient()
        elif gameplayMode == 'local':
            return LocalClient()
        else:
            raise ValueError('Invalid gameplay mode "{}", must be "browser", or "local"'.format(gameplayMode))

    def run(self, moveDelay=0.5):
        gameOver = False
        while not gameOver:
            time.sleep(moveDelay)
            gameOver = self.makeNextMove()
        # print('Game over')
        return self.client.getBoard()[0].getGrid()

    def makeNextMove(self):
        """
        Picks the direction of the next move and makes move.
        Returns:
        True if game is over, otherwise False
        """
        board, gameOver = self.client.getBoard()
        if not gameOver:
            nextMove = self.bot.getBestMove(board)
            if nextMove == 0:
                gameOver = True
            else:
                self.client.makeMove(nextMove)
        return gameOver
