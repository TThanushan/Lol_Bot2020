"""All functions for image processing"""
from PIL import ImageGrab
import cv2
import numpy as np
import utils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen(pos_x=0, pos_y=0, width=1920, height=1080, resize=1):
    """capture_screen(pos_x, pos_y, width, height, resize) -> image\n
    Return an screen capture under image format, you can resize it, 
    the resolution will be divided by resize"""
    #bbox specifies specific region (bbox= x,y,width,height)
    img = ImageGrab.grab(bbox = (pos_x, pos_y, width, height))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    if resize != 1:
        frame = cv2.resize(frame, (round(width/resize), round(height/resize)))
    return frame
    
def createTrackbar(name, win_name, value, count):
    def nothing(x):
        x += 0
    cv2.namedWindow(win_name)
    cv2.createTrackbar(name, win_name, value, count, nothing)    

def find_image_on_screen(image_name, threshold_value=0.99):
    capture = capture_screen()
    capture = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("ressources/"+image_name, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(capture, template, cv2.TM_CCOEFF_NORMED)
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



def apply_hsv_color_mask(frame, hsv_bound):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_b = np.array([hsv_bound["l_b"][0], hsv_bound["l_b"][1], hsv_bound["l_b"][2]])
    u_b = np.array([hsv_bound['u_b'][0], hsv_bound['u_b'][1], hsv_bound['u_b'][2]])
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

def is_obj_of_color_moving(obj_size, hsv_bound, pt1=(0, 0), pt2=(0, 0), \
    color=(0, 0, 0), resize=1):
    frame1 = capture_screen(resize=resize)
    frame2 = capture_screen(resize=resize)
    if np.any(pt2) != 0:
        hide_image_outer_area([frame1, frame2], pt1, pt2, color)
    frame1 = apply_hsv_color_mask(capture_screen(), hsv_bound)
    frame2 = apply_hsv_color_mask(capture_screen(), hsv_bound)
    return is_obj_moving(frame1, frame2, obj_size)

def hide_image_outer_area(frames, pt1, pt2, color=(0, 0, 0)):
    for frame in frames:
        cv2.rectangle(frame, (0, 0), (1920, pt1[1]), color, -1)
        cv2.rectangle(frame, (0, pt1[1]), (pt1[0], 1080), color, -1)
        cv2.rectangle(frame, (pt2[0], pt1[1]), (1920, 1080), color, -1)
        cv2.rectangle(frame, (0, pt2[1]), (1920, 1080), color, -1)

def img_to_text(img):
    return pytesseract.image_to_string(img, lang='eng', config='--psm 10 \
            --oem 3 -c tessedit_char_whitelist=0123456789')
    
def screen_text_to_string(TEXT_INFOS, reverse_color=True, hsv_bound=False):
    """Return digits from an area on the screen to string.\n
    Work only if the background color is lighter than the text color.\n
    If it is not the case, give a @mask list to apply, function will then
    reverse all the color to get lighter color in the background.
    """
    p1 = TEXT_INFOS["point1_location_area"]
    p2 = TEXT_INFOS["point2_location_area"]
    img = capture_screen(p1[0], p1[1], p2[0], p2[1])
    if hsv_bound is True:
        img = apply_hsv_color_mask(img, TEXT_INFOS)
    if reverse_color:
        img = cv2.bitwise_not(img)
    #text = pytesseract.image_to_string(img, lang='eng', config='--psm 10 \
            #--oem 3 -c tessedit_char_whitelist=0123456789')
    text = img_to_text(img)
    return text


def get_shapes_contours(shapes_hsv_bound):
    frame = capture_screen(resize=1.5)
    res = apply_hsv_color_mask(frame, shapes_hsv_bound)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_shapes_nb(shapes_hsv):
    occurence = 0
    contours = get_shapes_contours(shapes_hsv)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > shapes_hsv["min_size"] and contour_area < shapes_hsv["max_size"]:
            occurence += 1
    return occurence

def get_shapes_pos(shapes_hsv):
    positions = []
    contours = get_shapes_contours(shapes_hsv)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > shapes_hsv["min_size"] and contour_area < shapes_hsv["max_size"]:
            (x, y, w, h) = cv2.boundingRect(contour)
            positions.append([round(x+w/2), round(y+40)])
    return positions

