from image_functions import *
from game_object_const_info import *


def is_starting_on_left_side():
    return is_image_on_screen("minimap_mid_tower.png")

def is_enemy_champion_near_me():
    return get_shapes_nb(ENEMY_CHAMPIONS_INFOS) > 0

def is_allied_champion_near_me():
    return get_shapes_nb(ALLIED_CHAMPIONS_INFOS) > 0

def is_low_life():
    return not get_current_health() < 200

def get_nb_allied_champion():
    return get_shapes_nb(ALLIED_CHAMPIONS_INFOS)

def get_nb_enemy_champion():
    return get_shapes_nb(ENEMY_CHAMPIONS_INFOS)

def get_enemy_minion_pos():
    return get_shapes_pos(ENEMY_MINIONS_INFOS)

def get_nb_allied_minion():
    return get_shapes_nb(ALLIED_MINIONS_INFOS)

def get_nb_enemy_minion():
    return get_shapes_nb(ENEMY_MINIONS_INFOS)

def is_at_fountain():
    return is_image_on_screen("shop_button_highlighted.png")

def get_gold():
    text = screen_text_to_string(GOLD_TEXT_INFOS, True, True)
    if text is None or text == '':
        text = 0
    return int(text)

def get_current_health():
    text = screen_text_to_string(CURRENT_HEALTH_TEXT_INFOS, True, True)
    if text is None or text == '':
        text = 0
    return int(text)

def get_max_health():
    text = screen_text_to_string(MAX_HEALTH_TEXT_INFOS, True, True)
    if text is None or text == '':
        text = 0
    return int(text)


def get_current_mana():
    text = screen_text_to_string(CURRENT_MANA_TEXT_INFOS, True, True)
    if text is None or text == '':
        text = 0
    return int(text)

def get_max_mana():
    text = screen_text_to_string(MAX_MANA_TEXT_INFOS, True, True)
    if text is None or text == '':
        text = 0
    return int(text)

# def is_item_bought(size_v):
    # return is_obj_of_color_moving(size_v, 81, 88, 135, 87, 125, 255, (720, 887), (1034, 944), resize=4)
