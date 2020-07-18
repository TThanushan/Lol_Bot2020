from image_functions import *

# Bug: Think there is a enemey when looking at the herald health bar.
def get_nb_enemy_champion_on_screen():
    return get_nb_image_occurence_on_screen("enemy_champion_health_bar.png", 0.95)

def get_nb_ally_champion_on_screen():
    return get_nb_image_occurence_on_screen("ally_champion_health_bar.png", 0.98)

def is_starting_on_left_side():
    return is_image_on_screen("minimap_mid_tower.png")

def is_enemy_champion_near_me():
    return is_image_on_screen("enemy_champion_health_bar.png", 0.95)

def is_ally_champion_near_me():
    return is_image_on_screen("ally_champion_health_bar.png", 0.98)

def is_low_life():
    return not is_image_on_screen("low_life_indication.png", 0.96)

def get_minion_contours(obj_size, l_b, u_b):
    frame = capture_screen(resize=1.5)
    res = apply_hsv_color_mask(frame, l_b[0], l_b[1], l_b[2], u_b[0], u_b[1],\
            u_b[2])
    hide_image_outer_area(res, (240, 80), (960, 560))
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_minion_nb(obj_size, l_b, u_b):
    occurence = 0
    contours = get_minion_contours(obj_size, l_b, u_b)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > (obj_size) and contour_area < obj_size:
            occurence += 1
            print(occurence)
    return occurence

def get_minions_position(obj_size, l_b, u_b):
    ret = []
    contours = get_minion_contours(obj_size, l_b, u_b)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if (obj_size / 2) < contour_area < obj_size:
            (x, y, _, _) = cv2.boundingRect(contour)
            ret.append((round((x*1.5)+40), round((y*1.5)+60)))
    return ret

ALLY_MINIONS_HSV = {
    "size" : 500,
    "l_b" : [100, 160, 135],
    "u_b" : [105, 175, 190]
    }
ENEMY_MINIONS_HSV = {
    "size" : 500,
    "l_b" : [0, 120, 75],
    "u_b" : [0, 245, 185]
    }

def get_ally_minion_pos():
    return get_minions_position(ALLY_MINIONS_HSV["size"], ALLY_MINIONS_HSV["l_b"],\
             ALLY_MINIONS_HSV["u_b"])

def get_enemy_minion_pos():
    return get_minions_position(ENEMY_MINIONS_HSV["size"], ENEMY_MINIONS_HSV["l_b"],\
             ENEMY_MINIONS_HSV["u_b"])

def get_ally_minion_nb():
    return get_minion_nb(ALLY_MINIONS_HSV["size"], ALLY_MINIONS_HSV["l_b"],\
             ALLY_MINIONS_HSV["u_b"])

def get_enemy_minion_nb():
    return get_minion_nb(ENEMY_MINIONS_HSV["size"], ENEMY_MINIONS_HSV["l_b"],\
             ENEMY_MINIONS_HSV["u_b"])

def is_at_fountain():
    return is_image_on_screen("shop_button_highlighted.png")

# @utils.check_exec_time()
def get_gold():
    """Return current gold"""
    img = capture_screen()
    hide_image_outer_area([img], (1143, 1055), (1206, 1070))
    
    img = apply_hsv_color_mask(img, 0, 50, 75, 255, 255, 255)
    img = cv2.resize(img, (round(1920*1.5), round(1080*1.5)))
    img = cv2.bitwise_not(img)
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 10\
     --oem 3 -c tessedit_char_whitelist=0123456789')
    img = cv2.resize(img, (round(1920/2), round(1080/2)))
    if text == '':
        text = 0
    return int(text)

# def is_item_bought(size_v):
    # return is_obj_of_color_moving(size_v, 81, 88, 135, 87, 125, 255, (720, 887), (1034, 944), resize=4)
