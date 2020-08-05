import random
import time
import utils
import directkeys as dk
import other_class
import game_data

class Bot:
    """
    Bot class.
    """
    running = True
    shortcut = other_class.Shortcut()
    item_build = other_class.ItemBuild()
    GameData = game_data.GameData()
    action = "not set"
    is_do_once = False
    forward_pos = [0, 0]
    LEFT_FORWARD_POS = (1677, 894)
    RIGHT_FORWARD_POS = (1727, 839)

    def do_once(self):
        if not self.is_do_once:
            if self.GameData.is_left_side:
                self.forward_pos = self.LEFT_FORWARD_POS
            else:
                self.forward_pos = self.RIGHT_FORWARD_POS

    def wait(self, nb_secs=0.1):
        time.sleep(random.random() + nb_secs)

    def move_forward(self):
        dk.mouse_pos(self.forward_pos[0], self.forward_pos[1])
        dk.mouse_right_click()
