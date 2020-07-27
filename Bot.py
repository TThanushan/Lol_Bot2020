import directkeys as dk
import random
import time
import image_functions as imf
import threading
import utils
from other_class import *
from bot_functions import *

class Bot:
    """
    Bot class.
    """
    running = True
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
        self.screen_infos.current_health = get_current_health()
        self.screen_infos.allied_minions_nb = get_nb_allied_minion()
        self.screen_infos.enemy_champions_nb = get_nb_enemy_champion()
        self.screen_infos.current_health = get_current_health()

    def update_useful_data(self):
        self.screen_infos.allied_champions_nb = get_nb_allied_champion()
        self.screen_infos.enemy_minions_nb = get_nb_enemy_minion()
        self.screen_infos.max_health = get_max_health()
        self.screen_infos.current_mana = get_current_mana()
        self.screen_infos.max_mana = get_max_mana()

    def update_minor_data(self):
        self.screen_infos.is_at_fountain = is_at_fountain()
        self.screen_infos.gold = get_gold()

    def fast_thread(self):
        while self.running:
            self.update_crucial_data()

    def middle_thread(self):    
        while self.running:
            self.update_useful_data()

    def slow_thread(self):
        while self.running:
            self.update_minor_data()

    def behavior_loop(self):
        while self.running:
            if self.screen_infos.at_fountain:
                self.item_build.try_to_buy_current_item()
                self.move_forward()
                time.sleep(2)
                if self.screen_infos.allied_minions_nb:
                    print("bip")
