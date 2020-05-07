from PIL import ImageGrab, ImageOps
import pyautogui
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
from tiles import TILES, TILE_COORDINATES
from gameboard import GameBoard
import time

class GameClient:
    def __init__(self):
        self.board = GameBoard()
        self.tiles = TILES
        self.gameOver = False

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
        self.selectGameWindow()

    def selectGameWindow(self):
        """
        Selects the browser window containing the 2048 game using the mouse
        """
        pyautogui.click(self.getWindowCoordinates())

    def getBoard(self):
        """
        Gets the tile value for each tile in the grid
        """
        self.window = ImageGrab.grab()

        for index, coord in enumerate(TILE_COORDINATES):
            try:
                self.board.setTile(index, self.getTileValue(coord))
            except KeyError:
                print(coord)
                self.gameOver = True
                break
        return self.board, self.gameOver

    def makeMove(self, direction):
        pyautogui.keyDown(KEYMAP[direction])
        time.sleep(0.01)
        pyautogui.keyUp(KEYMAP[direction])
        self.updateScore(direction)

    def getTileValue(self, tileCoordinates):
        """
        Gets a the value of a tile given its coordinates

        Args:
        tileCoordinates: (x, y) coordinates of a tile on screen

        Returns:
        The integer value on the tile
        """
        return self.tiles[self.window.getpixel(tileCoordinates)]

    def getWindowCoordinates(self):
        """
        Returns (x, y) coordinates of the tile grid on the window.
        This is used by the bot to select the correct window
        """
        return TILE_COORDINATES[0]

class LocalClient(GameClient):
    def __init__(self):
        super().__init__()
