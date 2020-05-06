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

    def getGrid(self):
        """
        Gets the tile value for each tile in the grid
        """
        self.window = ImageGrab.grab()
        for index, coord in enumerate(TILE_COORDINATES):
            self.board.setTile(index, self.getTileValue(coord))

    def printGrid(self):
        for i in range(16):
            if i % 4 == 0:
                print("[ " + str(grid.getTile(i)) + " " + str(grid.getTile(i+1)) + " " + str(grid.getTile(i+2)) + " " + str(grid.getTile(i+3)) + " ]")

    def move(self, direction):
        """
        Makes a move on the 2048 board in a direction (Left, Right, Up, Down)
        """
        pass

    def getTileValue(self, tileCoordinates):
        """
        Gets a the value of a tile given its coordinates

        Args:
        tileCoordinates: (x, y) coordinates of a tile on screen

        Returns:
        The integer value on the tile
        """
        return self.tiles[self.window.getPixel(tileCoordinates)]

    def getWindowCoordinates(self):
        """
        Returns (x, y) coordinates of the tile grid on the window.
        This is used by the bot to select the correct window
        """
        return TILE_COORDINATES[0]
