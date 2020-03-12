import directkeys as dk
import random
import time
import image_functions as imf
import threading
class Bot:
    """
    Bot class.
    """
    shortcut = {
        "spell 1" : 'q',
        "spell 2" : 'w',
        "spell 3" : 'e',
        "spell ult" : 'r',
        "move attack" : ' ',
        "toggle shop" : 'p'
    }
    #index : [name, price]
    items_build = {
        0 : ["doran's shield", 450],
        1 : ["warding totem", 0],
        2 : ["ninja tabi", 1100],
        3 : ["phage", 1250],
        4 : ["sheen", 1050],
        5 : ["stinger", 1100],
        6 : ["trinity force", 333],
        7 : ["jaurim's fist", 1200],
        8 : ["pickaxe", 875],
        9 : ["sterak's gage", 725],
        10 : ["spirit visage", 2800],
        11 : ["dead man's plat", 2900],
        # 12 : ["thornmail", 2900],
    }
    screen_infos = {
        "a_minions" : False,
        "a_champions" : False,
        "e_minions" : False,
        "e_champions" : False,
        "low_life" : False,
        "at_fountain" : False,
        "gold" : 0
    }
    action = "not set"
    pause = False
    item_index = 0
    champ_name = "Darius"
    is_left_side = False
    is_do_once = False
    forward_pos = [0, 0]
    LEFT_FORWARD_POS = (1677, 894)
    RIGHT_FORWARD_POS = (1727, 839)
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
            self.buy_starter_items()
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
        self.buy_item(self.items_build[0][0])
        self.buy_item(self.items_build[1][0])
    def move_forward(self):
        dk.mouse_pos(self.forward_pos[0], self.forward_pos[1])
        dk.mouse_right_click()
    def update_screen_infos(self):
        while True:
            self.screen_infos["a_minions"] = imf.is_ally_minions_near_me()
            self.screen_infos["a_champions"] = imf.is_ally_champion_near_me()
            self.screen_infos["e_minions"] = imf.is_enemy_minions_near_me()
            self.screen_infos["e_champions"] = imf.is_enemy_champion_near_me()
            self.screen_infos["low_life"] = imf.is_low_life()
            self.screen_infos["at_fountain"] = imf.is_at_fountain()
            self.screen_infos["gold"] = imf.get_gold()
    def behavior_loop(self):
        if self.screen_infos["at_fountain"]:
            self.move_forward()

    active_time = property(_get_active_time, _set_active_time)
        