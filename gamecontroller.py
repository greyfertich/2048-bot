import pyautogui
from gamebot import GameBot
from gameclient import GameClient
from directions import LEFT, RIGHT, UP, DOWN, KEYMAP
import time

class GameController:

    def __init__(self):
        self.client = GameClient()
        self.bot = GameBot(self.client)
        self.selectGameWindow()

    def run(self):
        while True:
            self.bot.updateBoard()
            self.makeNextMove(moveDelay=0)

    def makeNextMove(self, moveDelay=1):
        """
        Picks the direction of the next move and makes move
        """
        time.sleep(moveDelay)
        nextMove = self.bot.getBestMove()
        pyautogui.keyDown(KEYMAP[nextMove])
        time.sleep(0.01)
        pyautogui.keyUp(KEYMAP[nextMove])
        self.bot.updateBoard()

    def selectGameWindow(self):
        """
        Selects the window containing the 2048 game using the mouse
        """
        pyautogui.click(self.client.getWindowCoordinates())
