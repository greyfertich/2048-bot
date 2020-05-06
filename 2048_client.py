from PIL import ImageGrab, ImageOps
import pyautogui
import directions, tiles

class GameClient:
    def __init__(self):
        self.tiles = tiles
        self.grid = [0 for _ in range(16)]

    def getGrid(self):
        """
        Gets the tile value for each tile in the grid
        """
        window = ImageGrab.grab()
        for index, coord in enumerate(TILE_COORDINATES):
            self.grid[index] = self.tiles[window.getpixel(coord)]

    def printGrid(self):
        for i in range(16):
            if i % 4 == 0:
                print("[ " + str(grid[i]) + " " + str(grid[i+1]) + " " + str(grid[i+2]) + " " + str(grid[i+3]) + " ]")

    def makeMove(self, direction):
        """
        Makes a move on the 2048 board in a direction (Left, Right, Up, Down)
        """
        pass

    def getTileFromGrid(self, tileIndex):
        pass
