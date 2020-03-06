"""All functions for image processing"""
import cv2
from PIL import ImageGrab
import numpy as np

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

while True:
    # location = get_image_on_screen_pos("enemy_champion_health_bar.png", 0.95)
    location = get_nb_enemy_champion_on_screen()
    print(str(get_nb_ally_champion_on_screen()))
    # print(str(np.size(location)))
    # img = capture_screen()
    # img_read = cv2.imread("ressources/enemy_champion_health_bar.png", 0)
    # w, h = img_read.shape[::-1]
    # if location is not None:
    #     print(str(location[0][0])+"|"+str(location[1][0]))
    #     cv2.rectangle(img, (location[1][0], location[0][0]), (location[1][0] + w, location[0][0] + h), (0, 0, 255), 2)
    # cv2.imshow("img", img)
    # if cv2.waitKey(40) == 27:
    #     break

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
        if contour_area > obj_size and contour_area < obj_size * 1.7:
            return True
    return False

def is_obj_of_color_moving(obj_size, l_h, l_s, l_v, u_h, u_s, u_v):
    frame1 = capture_screen(resize=2)
    frame2 = capture_screen(resize=2)
    frame1 = apply_hsv_color_mask(capture_screen(resize=2), l_h, l_s, l_v, u_h, u_s, u_v)
    frame2 = apply_hsv_color_mask(capture_screen(resize=2), l_h, l_s, l_v, u_h, u_s, u_v)
    return is_obj_moving(frame1, frame2, obj_size)

def is_ally_minions_near_me():
    return is_obj_of_color_moving(300, 100, 155, 90, 105, 170, 225)
# while True:
    # print(is_ally_minions_near_me())
# main3()