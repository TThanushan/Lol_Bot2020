"""Contains all functions that allow to retrieve game data"""

import image_functions as imf
import game_object_const_info as const_info

class GameData:
    """
    Contains game data.
    """
    is_left_side = False
    current_health = 0
    max_health = 0
    current_mana = 0
    max_mana = 0
    allied_minions_nb = 0
    allied_champions_nb = 0
    enemy_minions_nb = 0
    enemy_champions_nb = 0
    is_at_fountain = False
    gold = 0
    allied_minions = []
    def get_all_properties(self):
        return {
            "Health" : str(self.current_health) + " / " + str(self.max_health),
            "Mana" : str(self.current_mana) + " / " + str(self.max_mana),        
            "Allied minions" : self.allied_minions_nb,
            "Allied champions" : self.allied_champions_nb,
            "Enemy minions" : self.enemy_minions_nb,
            "Enemy champions" : self.enemy_champions_nb,
            "is low life" : self.current_health < 200,
            "is at fountain" : self.get_is_at_fountain,
            "gold" : self.gold
            }
    
    def update_all_data(self):
        self.current_health = self.get_current_health()
        self.enemy_champions_nb = self.get_nb_enemy_champion()
        self.allied_minions_nb = self.get_nb_allied_minion()
        self.allied_minions = self.get_allied_minions()
        self.allied_champions_nb = self.get_nb_allied_champion()
        self.enemy_minions_nb = self.get_nb_enemy_minion()
        self.current_mana = self.get_current_mana()
        self.max_health = self.get_max_health()
        self.max_mana = self.get_max_mana()
        self.is_at_fountain = self.get_is_at_fountain()
        self.gold = self.get_gold()

    def is_starting_on_left_side(self):
        return imf.is_image_on_screen("minimap_mid_tower.png")

    def is_enemy_champion_near_me(self):
        return imf.get_shapes_nb(const_info.ENEMY_CHAMPIONS_INFOS) > 0

    def is_allied_champion_near_me(self):
        return imf.get_shapes_nb(const_info.ALLIED_CHAMPIONS_INFOS) > 0

    def is_low_life(self):
        return self.get_current_health() < 350

    def get_nb_allied_champion(self):
        return imf.get_shapes_nb(const_info.ALLIED_CHAMPIONS_INFOS)

    def get_nb_enemy_champion(self):
        return imf.get_shapes_nb(const_info.ENEMY_CHAMPIONS_INFOS)

    def get_enemy_minion_pos(self):
        return imf.get_shapes_pos(const_info.ENEMY_MINIONS_INFOS)

    def get_nb_allied_minion(self):
        return imf.get_shapes_nb(const_info.ALLIED_MINIONS_INFOS)

    def get_allied_minions(self):
        return imf.get_shapes_pos(const_info.ALLIED_MINIONS_INFOS)

    def get_nb_enemy_minion(self):
        return imf.get_shapes_nb(const_info.ENEMY_MINIONS_INFOS)

    def get_is_at_fountain(self):
        return imf.is_image_on_screen("shop_button_highlighted.png")

    def get_gold(self):
        text = imf.screen_text_to_string(const_info.GOLD_TEXT_INFOS, True, True)
        if text is None or text == '':
            text = 0
        return int(text)

    def get_current_health(self):
        text = imf.screen_text_to_string(const_info.CURRENT_HEALTH_TEXT_INFOS,\
            True, True)
        if text is None or text == '':
            text = 0
        return int(text)

    def get_max_health(self):
        text = imf.screen_text_to_string(const_info.MAX_HEALTH_TEXT_INFOS,\
            True, True)
        if text is None or text == '':
            text = 0
        return int(text)

    def get_current_mana(self):
        text = imf.screen_text_to_string(const_info.CURRENT_MANA_TEXT_INFOS,\
            True, True)
        if text is None or text == '':
            text = 0
        return int(text)

    def get_max_mana(self):
        text = imf.screen_text_to_string(const_info.MAX_MANA_TEXT_INFOS, True,\
             True)
        if text is None or text == '':
            text = 0
        return int(text)

# def is_item_bought(size_v):
    # return is_obj_of_color_moving(size_v, 81, 88, 135, 87, 125, 255, (720, 887), (1034, 944), resize=4)
