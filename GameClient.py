from PIL import ImageGrab, ImageOps
import pyautogui
import directions, tiles

class GameClient:
    def __init__(self):
        self.tiles = tiles
        self.grid = [0 for _ in range(16)]
        self.window = None

    def getGrid(self):
        """
        Gets the tile value for each tile in the grid
        """
        self.window = ImageGrab.grab()
        for index, coord in enumerate(TILE_COORDINATES):
            self.grid[index] = self.getTileValue(coord)

    def printGrid(self):
        for i in range(16):
            if i % 4 == 0:
                print("[ " + str(grid[i]) + " " + str(grid[i+1]) + " " + str(grid[i+2]) + " " + str(grid[i+3]) + " ]")

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
