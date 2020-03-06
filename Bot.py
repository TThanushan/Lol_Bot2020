import directkeys as dk
import random
import time
import image_functions as imf
class Bot:
    """
    Bot class.
    """
    champ_name = "Darius"
    shortcut = {
        "spell 1" : 'q',
        "spell 2" : 'w',
        "spell 3" : 'e',
        "spell ult" : 'r',
        "move attack" : ' ',
        "toggle shop" : 'p'
    }
    is_left_side = False
    is_do_once = False
    forward_pos = [0, 0]
    LEFT_FORWARD_POS = (1677, 894)
    RIGHT_FORWARD_POS = (1727, 839)
    items_build = (
        "doran's shield",
        "warding totem",
        "ninja tabi"
        "phage",
        "sheen",
        "stinger",
        "trinity force",
        "jaurim's fist",
        "pickaxe",
        "sterak's gage",
        "spirit visage",
        "dead man's plat",
        "thornmail",
    )
    item_index = 0
    def __init__(self):
        self._active_time = 0
        print("Bot", self.champ_name, "initiated!")
    def _get_active_time(self):
        return self._active_time
    def _set_active_time(self, value):
        self._active_time = value
        print("active time modified !")
    def do_once(self):
        if not self.is_do_once:
            self.is_left_side = imf.is_starting_on_left_side()
            if self.is_left_side:
                self.forward_pos = self.LEFT_FORWARD_POS
            else:
                self.forward_pos = self.RIGHT_FORWARD_POS
                
    def wait(self, nb_secs=0.1):
        time.sleep(random.random() + nb_secs)
    def buy_item(self, item_name):
        """
        Try to buy an item from the shop by typing the name.
        """
        #Press p to open shop
        dk.PressKey(self.shortcut["toggle shop"])
        # #Press ctrl+L to select search bar
        dk.MaintainKey('ctrl')
        dk.PressKey('l')
        dk.ReleaseKey('ctrl')
        #Type starter item name Doran shield
        dk.type_text(item_name)
        # Press enter twice to buy
        dk.PressKey("enter")
        dk.PressKey("enter")
        #Press esc to close shop
        dk.PressKey('esc')
    def buy_starter_items(self):
        self.buy_item("doran's shield")
        self.buy_item("health potion")
        self.buy_item("warding totem")
    def move_forward(self):
        dk.mouse_right_click()
    def main_loop(self):
        #buy lvl 1 items
        self.buy_starter_items()
        self.move_forward()
    active_time = property(_get_active_time, _set_active_time)
        