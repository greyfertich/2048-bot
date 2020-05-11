from PIL import ImageGrab, ImageOps
import pyautogui
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from tiles import TILES, TILE_COORDINATES, getTileFromColor
from game import Game2048, GameState
import time

class GameClient:
    def __init__(self):
        self.game = Game2048()
        self.tiles = TILES
        self.gameOver = False
        self.initializeGame()

    def initializeGame(self):
        pass

    def getBoard(self):
        pass

    def updateBoard(self):
        """
        Gets the tile value for each tile in the grid
        """
        pass

    def makeMove(self, direction):
        pass

    def getTileValue(self, tileCoordinates):
        """
        Gets a the value of a tile given its coordinates

        Args:
        tileCoordinates: (x, y) coordinates of a tile on screen

        Returns:
        The integer value on the tile
        """
        pass

    def updateScore(self, direction):
        self.board.updateScore(direction)

    def getScore(self):
        return self.board.getScore()

    def isGameOver(self):
        return self.gameOver


class BrowserClient(GameClient):
    def __init__(self):
        super().__init__()
        self.window = None

    def initializeGame(self):
        """
        Selects the browser window containing the 2048 game using the mouse
        """
        pyautogui.click(self.getWindowCoordinates())

    def getBoard(self):
        """
        Gets the tile value for each tile in the grid
        """
        self.window = ImageGrab.grab()

        newGrid = [0 for _ in range(16)]

        for index, coord in enumerate(TILE_COORDINATES):
            try:
                newGrid[index] = self.getTileValue(coord)
                state = GameState(newGrid, 0, self.gameOver)
                self.game = Game2048(prev_state=state)
            except KeyError:
                print(self.window.getpixel(coord))
                self.gameOver = True
                break
        return self.game, self.gameOver

    def makeMove(self, direction):
        #TODO: update score tracking in new game
        pyautogui.keyDown(KEYMAP[direction])
        time.sleep(0.01)
        pyautogui.keyUp(KEYMAP[direction])
        #self.updateScore(direction)

    def getTileValue(self, tileCoordinates):
        """
        Gets a the value of a tile given its coordinates

        Args:
        tileCoordinates: (x, y) coordinates of a tile on screen

        Returns:
        The integer value on the tile
        """
        return getTileFromColor(self.window.getpixel(tileCoordinates))

    def getWindowCoordinates(self):
        """
        Returns (x, y) coordinates of the tile grid on the window.
        This is used by the bot to select the correct window
        """
        return TILE_COORDINATES[0]

class LocalClient(GameClient):
    def __init__(self):
        super().__init__()

    def getBoard(self):
        return self.game, self.game.isGameOver()

    def makeMove(self, direction):
        self.game.moveAndPlaceRandomTile(direction)
        self.gameOver = self.game.isGameOver()
        print('Score: {}'.format(self.game.getScore()))
        self.game.printBoard()
