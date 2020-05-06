import pyautogui
import directions
import time

class GameBot:

    def __init__(self, gameClient):
        self.client = gameClient
        self.selectGameWindow()
        while True:
            self.makeNextMove()

    def makeNextMove(self):
        """
        Picks the direction of the next move and makes move
        """
        time.sleep(1)
        pyautogui.keyDown('left')
        time.sleep(0.05)
        pyautogui.keyUp('left')
        time.sleep(1)
        pyautogui.keyDown('right')
        time.sleep(0.05)
        pyautogui.keyUp('right')

    def findMove(self):
        """
        Finds the direction of the next move
        """
        grid = self.client.getGrid()

    def selectGameWindow(self):
        """
        Selects the window containing the 2048 game using the mouse
        """
        pyautogui.click(self.client.getWindowCoordinates())
