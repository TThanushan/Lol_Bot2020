import directkeys as dk
import random
import time

class Bot:
    """
    Bot class.
    """
    champ_name = "Darius"

    def __init__(self):
        self._active_time = 0
        print("Bot", self.champ_name, "initiated!")

    def _get_active_time(self):
        return self._active_time

    def _set_active_time(self, value):
        self._active_time = value
        print("active time modified !")
    def wait(self):
        time.sleep(random.random() + 0.1)
    def buy_item(self, item_name):
        """
        Try to buy an item from the shop by typing the name.
        """
        #Press p to open shop
        dk.PressKey('p')
        self.wait()
        # #Press ctrl+L to select search bar
        dk.MaintainKey('ctrl')
        dk.PressKey('l')
        dk.ReleaseKey('ctrl')
        #Type starter item name Doran shield
        dk.type_text(item_name)
        # Press enter twice to buy
        self.wait()
        dk.PressKey("enter")
        self.wait()
        dk.PressKey("enter")
        self.wait()
        #Press esc to close shop
        dk.PressKey('esc')
        self.wait()
    active_time = property(_get_active_time, _set_active_time)
        