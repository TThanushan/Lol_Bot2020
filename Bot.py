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

    def do_once(self):
        if not self.is_do_once:
            # self.buy_starter_items()
            self.is_left_side = imf.is_starting_on_left_side()
            if self.is_left_side:
                self.forward_pos = self.LEFT_FORWARD_POS
            else:
                self.forward_pos = self.RIGHT_FORWARD_POS

    def wait(self, nb_secs=0.1):
        time.sleep(random.random() + nb_secs)

    def move_forward(self):
        dk.mouse_pos(self.forward_pos[0], self.forward_pos[1])
        dk.mouse_right_click()

    def update_crucial_data(self):
        self.screen_infos.low_life = imf.is_low_life()
        self.screen_infos.ally_minions = imf.get_a_minion_nb()
        self.screen_infos.enemy_champions = imf.is_enemy_champion_near_me()

    def update_useful_data(self):
        self.screen_infos.ally_champions = imf.is_ally_champion_near_me()
        self.screen_infos.enemy_minions = imf.get_e_minion_nb()

    def update_minor_data(self):
        self.screen_infos.at_fountain = imf.is_at_fountain()
        self.screen_infos.gold = imf.get_gold()

    def fast_thread(self):
        while True:
            self.update_crucial_data()

    def middle_thread(self):    
        while True:
            self.update_useful_data()

    def slow_thread(self):
        while True:
            self.update_minor_data()

    def behavior_loop(self):
        while True:
            if self.screen_infos.at_fountain:
                self.item_build.try_to_buy_current_item()
                self.move_forward()
                time.sleep(2)
                if self.screen_infos.ally_minions:
                    print("bip")
