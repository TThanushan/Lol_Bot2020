import pynput
from pynput.keyboard import Key
from pynput.mouse import Button

class Bot:
    """
    Bot class.
    """
    champ_name = "Darius"
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    def __init__(self):
        self._active_time = 0
        print("Bot", self.champ_name, "initiated!")

    def _get_active_time(self):
        return self._active_time

    def _set_active_time(self, value):
        self._active_time = value
        print("active time modified !")

    def buy_item(self, item_name):
        """
        Try to buy an item from the shop by typing the name.
        """
        #Press p to open shop
        self.keyboard.press('q')
        # #Press ctrl+L to select search bar
        # self.keyboard.press(Key.ctrl)
        # self.keyboard.press('p')
        # self.keyboard.release(Key.ctrl)
        # #Type starter item name Doran shield
        # self.keyboard.type(item_name)
        # #Move mouse then click on the item icon
        # self.mouse.position = (500, 500)
        # self.mouse.click(Button.left)
        self.keyboard.type('p')
        #Press p to close shop

    active_time = property(_get_active_time, _set_active_time)
