"""All functions for image processing"""
import cv2
from PIL import ImageGrab
import numpy as np

def capture_screen(pos_x=0, pos_y=0, width=1920, height=1080, resize=1):
    """capture_screen(pos_x, pos_y, width, height, resize) -> image

    Return an screen capture under image format, you can resize it, the resolution will be divided by resize"""
    #bbox specifies specific region (bbox= x,y,width,height)
    img = ImageGrab.grab(bbox=(pos_x, pos_y, width, height))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return cv2.resize(frame, (round(width/resize), round(height/resize)))

def apply_color_mask(image, lower=0, upper=0):
    lower = np.array((240, 240, 240), dtype="uint8")
    upper = np.array((255, 255, 255), dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    return output

def createTrackbar(name, win_name, value, count):
    def nothing(x):
        print(x)
    cv2.namedWindow(win_name)
    cv2.createTrackbar(name, win_name, value, count, nothing)    

def get_starting_side():
    createTrackbar("threshold", "image", 100, 100)
    while True:
        capture = capture_screen()
        grey_img = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("ressources/minimap_mid_tower.png", 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        threshold = cv2.getTrackbarPos("threshold", "image") / 100
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(capture, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # capture = cv2.resize(capture, (round(1920/6), round(1080/6)))
        capture = cv2.resize(capture, (round(1920/2), round(1080/2)))
        cv2.imshow("image", capture)
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()

get_starting_side()
