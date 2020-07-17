import directkeys as dk
import random
import time
import image_functions as imf
import threading
import utils
from other_class import *
class Bot:
    """
    Bot class.
    """
    shortcut = Shortcut()
    item_build = ItemBuild()
    screen_infos = ScreenInfos()
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
            # self.buy_starter_items()
            self.is_left_side = imf.is_starting_on_left_side()
            if self.is_left_side:
                self.forward_pos = self.LEFT_FORWARD_POS
                print("left side")
            else:
                self.forward_pos = self.RIGHT_FORWARD_POS
                print("right side")

    def wait(self, nb_secs=0.1):
        time.sleep(random.random() + nb_secs)

    def get_item_price(self):
        return self.items_build[self.item_build.current_index[1]]

    def get_item_name(self):
        return self.items_build[self.item_index][0]

    @utils.check_exec_time()
    def buy_items(self):
        """
        Try to buy an item from the shop by typing the name.
        """
        #Press p to open shop
        self.screen_infos["gold"] = imf.get_gold()
        if self.screen_infos["gold"] >= self.get_item_price():
            dk.PressKey(self.shortcut["toggle shop"])
            while self.screen_infos["gold"] >= self.get_item_price():
                # #Press ctrl+L to select search bar
                dk.MaintainKey('ctrl')
                dk.PressKey('l')
                dk.ReleaseKey('ctrl')
                #Type starter item name Doran shield
                dk.type_text(self.get_item_name())
                # Press enter twice to buy
                dk.PressKey("enter")
                time.sleep(0.1 + random.random())
                dk.PressKey("enter")
                time.sleep(0.1 + random.random())
                self.screen_infos["gold"] -= self.get_item_price() 
                self.item_index += 1
                if self.item_index not in self.items_build:
                    break
                # print("item nb :"+str(self.item_index))
                # print("gold :"+str(self.screen_infos["gold"]))
            #Press esc to close shop
            dk.PressKey('esc')

    def move_forward(self):
        dk.mouse_pos(self.forward_pos[0], self.forward_pos[1])
        dk.mouse_right_click()

    def fast_thread(self):
        while True:
            self.screen_infos["low_life"] = imf.is_low_life()
            self.screen_infos["a_minions"] = imf.get_a_minion_nb()
            self.screen_infos["e_champions"] = imf.is_enemy_champion_near_me()
            print(str(self.screen_infos["a_minions"]))
            print(str(self.screen_infos["e_minions"]))

    def middle_thread(self):    
        while True:
            self.screen_infos["low_life"] = imf.is_low_life()
            self.screen_infos["a_champions"] = imf.is_ally_champion_near_me()
            self.screen_infos["e_minions"] = imf.get_e_minion_nb()

    def slow_thread(self):
        while True:
            self.screen_infos["at_fountain"] = imf.is_at_fountain()
            self.screen_infos["gold"] = imf.get_gold()

    def behavior_loop(self):
        while True:
            if self.screen_infos["at_fountain"]:
                self.buy_items()
                self.move_forward()
                time.sleep(2)
                if self.screen_infos["a_minions"]:
                    print("bip")

    active_time = property(_get_active_time, _set_active_time)
        