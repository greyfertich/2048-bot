from PIL import ImageGrab, ImageOps
import pyautogui
from directions import LEFT, RIGHT, UP, DOWN
from tiles import TILES, TILE_COORDINATES
from gameboard import GameBoard

class GameClient:
    def __init__(self):
        self.board = GameBoard()
        self.tiles = TILES
        self.window = None
        self.gameOver = False

    def getBoard(self):
        return self.board

    def readBoardFromWindow(self):
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
    def printGrid(self, grid):
        for i in range(16):
            if i % 4 == 0:
                print("[ " + str(grid[i]) + " " + str(grid[i+1]) + " " + str(grid[i+2]) + " " + str(grid[i+3]) + " ]")

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

    def isGameOver(self):
        return self.gameOver
