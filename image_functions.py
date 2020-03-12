"""All functions for image processing"""
import cv2
from PIL import ImageGrab
import numpy as np
import utils
import pytesseract

def capture_screen(pos_x=0, pos_y=0, width=1920, height=1080, resize=1):
    """capture_screen(pos_x, pos_y, width, height, resize) -> image\n
    Return an screen capture under image format, you can resize it, 
    the resolution will be divided by resize"""
    #bbox specifies specific region (bbox= x,y,width,height)
    img = ImageGrab.grab(bbox=(pos_x, pos_y, width, height))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return cv2.resize(frame, (round(width/resize), round(height/resize)))

def createTrackbar(name, win_name, value, count):
    def nothing(x):
        print(x)
    cv2.namedWindow(win_name)
    cv2.createTrackbar(name, win_name, value, count, nothing)    

def find_image_on_screen(image_name, threshold_value=0.99):
    capture = capture_screen()
    grey_img = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("ressources/"+image_name, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
    threshold = threshold_value
    return np.where(res >= threshold)
    
def is_image_on_screen(image_name, threshold_value=0.99):
    loc = find_image_on_screen(image_name, threshold_value)
    if np.any(loc) != 0:
        return True
    return False

def get_image_on_screen_pos(image_name, threshold_value=0.99):
    loc = find_image_on_screen(image_name, threshold_value)
    if np.any(loc) != 0:
        return (loc[0], loc[1])
    return None

def get_nb_image_occurence_on_screen(image_name, threshold_value=0.99):
    loc = find_image_on_screen(image_name, threshold_value)
    pt_y_save = 0
    nb = 0
    for pt in zip(*loc[::-1]):
        # I don't increment if the occurrence y pos is on the same as the other.
        if pt[1] != pt_y_save:
            nb += 1
            pt_y_save = pt[1]
    return nb

# Think there is a enemey when looking at the herald health bar.
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
def get_moving_object_by_size(size_wanted=1000):
    """Get position of a moving object that's equal to the size given
    in parameter"""
    frame1 = capture_screen()
    frame2 = capture_screen()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < size_wanted:
            return contour
    return None

def apply_hsv_color_mask(frame, l_h, l_s, l_v, u_h, u_s, u_v):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, l_b, u_b)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res

def is_obj_moving(frame, next_frame, obj_size):
    diff = cv2.absdiff(frame, next_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > obj_size and contour_area < obj_size * 1.3:
            return True
    return False

def is_obj_of_color_moving(obj_size, l_h, l_s, l_v, u_h, u_s, u_v, pt1=(0, 0), pt2=(0, 0), \
    color=(0, 0, 0), resize=1):
    frame1 = capture_screen(resize=resize)
    frame2 = capture_screen(resize=resize)
    print(str(resize))
    if np.any(pt2) != 0:
        hide_image_outer_area([frame1, frame2], pt1, pt2, color)
    # frame1 = apply_hsv_color_mask(capture_screen(), l_h, l_s, l_v, u_h, u_s, u_v)
    # frame2 = apply_hsv_color_mask(capture_screen(), l_h, l_s, l_v, u_h, u_s, u_v)
    return is_obj_moving(frame1, frame2, obj_size)
def hide_image_outer_area(frames, pt1, pt2, color=(0, 0, 0)):
    for frame in frames:
        cv2.rectangle(frame, (0, 0), (1920, pt1[1]), color, -1)
        cv2.rectangle(frame, (0, pt1[1]), (pt1[0], 1080), color, -1)
        cv2.rectangle(frame, (pt2[0], pt1[1]), (1920, 1080), color, -1)
        cv2.rectangle(frame, (0, pt2[1]), (1920, 1080), color, -1)
def is_ally_minions_near_me():
    return is_obj_of_color_moving(300, 100, 155, 90, 105, 170, 225)

def is_enemy_minions_near_me():
    return is_obj_of_color_moving(300, 0, 130, 160, 4, 170, 225)
def is_at_fountain():
    return is_image_on_screen("shop_button_highlighted.png")
def screen_text_to_string(area_pt1, area_pt2, reverse_color=False, mask=None):
    """Return digits from an area on the screen to string.\n
    Work only if the background color is lighter than the text color.\n
    If it is not the case, give a @mask list to apply, function will then
    reverse all the color to get lighter color in the background.
    """
    img = capture_screen()
    hide_image_outer_area([img], area_pt1, area_pt2)
    if reverse_color:
        img = apply_hsv_color_mask(img, mask[0], mask[1], mask[2], mask[3], \
                                   mask[4], mask[5])
        img = cv2.bitwise_not(img)
    text = pytesseract.image_to_string(img)
    return text
def get_gold():
    """Return current gold"""
    return screen_text_to_string((1143, 1055), (1206, 1067),\
         reverse_color=True, mask=[0, 0, 115, 50, 110, 255])

# def is_item_bought(size_v):
    # return is_obj_of_color_moving(size_v, 81, 88, 135, 87, 125, 255, (720, 887), (1034, 944), resize=4)
    
# while True:
#     print(str(is_item_bought(240)))
#     # print(str(is_at_fountain()))
# def main2():
#     createTrackbar("size", "win2", 0, 1500)
#     size = cv2.getTrackbarPos("size", "win2")
#     frame1 = capture_screen()
#     frame2 = capture_screen()
#     while (True):
#         hide_image_outer_area([frame1, frame2], (720, 887), (1034, 944), (255, 255, 255))
#         # frame1 = apply_hsv_color_mask(frame1, 81, 88, 135, 87, 125, 255)
#         # frame2 = apply_hsv_color_mask(frame2, 81, 88, 135, 87, 125, 255)
#         diff = cv2.absdiff(frame1, frame2)
#         gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (5, 5), 0)
#         _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#         dilated = cv2.dilate(thresh, None, iterations=3)
#         contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         size = cv2.getTrackbarPos("size", "win2")
#         for contour in contours:
#             (x, y, w, h) = cv2.boundingRect(contour)
#             obj_size = cv2.contourArea(contour)
#             if obj_size > size and obj_size < size * 1.3:
#                 cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.imshow("inter", frame1)
#         frame1 = frame2
#         frame2 = capture_screen()
#         if cv2.waitKey(40) == 27:
#             break
#     cv2.destroyAllWindows()
# main2()
