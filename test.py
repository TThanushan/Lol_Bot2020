"""Test"""
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import directkeys as dk
from image_functions import *
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SHAPE_INFOS = {
    "point1_location_area" : [1167, 1051],
    "point2_location_area" : [1240, 1070],
    "l_b" : [0, 50, 75],
    "u_b" : [255, 255, 255]
    } 

def create_trackbars():
    createTrackbar("LH", "win2", SHAPE_INFOS["l_b"][0], 255)
    createTrackbar("LS", "win2", SHAPE_INFOS["l_b"][1], 255)
    createTrackbar("LV", "win2", SHAPE_INFOS["l_b"][2], 255)
    
    createTrackbar("UH", "win2", SHAPE_INFOS["u_b"][0], 255)
    createTrackbar("US", "win2", SHAPE_INFOS["u_b"][1], 255)
    createTrackbar("UV", "win2", SHAPE_INFOS["u_b"][2], 255)

def get_trackbars_values():
    SHAPE_INFOS["l_b"][0] = cv2.getTrackbarPos("LH", "win2")
    SHAPE_INFOS["l_b"][1] = cv2.getTrackbarPos("LS", "win2")
    SHAPE_INFOS["l_b"][2] = cv2.getTrackbarPos("LV", "win2")
        
    SHAPE_INFOS["u_b"][0] = cv2.getTrackbarPos("UH", "win2")
    SHAPE_INFOS["u_b"][1] = cv2.getTrackbarPos("US", "win2")
    SHAPE_INFOS["u_b"][2] = cv2.getTrackbarPos("UV", "win2")

def get_text_from_screen_test():

    create_trackbars()
    while True:
        p1 = SHAPE_INFOS["point1_location_area"]
        p2 = SHAPE_INFOS["point2_location_area"]
        img = capture_screen(p1[0], p1[1], p2[0], p2[1])
        get_trackbars_values()
        img = apply_hsv_color_mask(img, SHAPE_INFOS)
        dst_size = (p1[1] - p1[0], p2[1] - p2[0])
        img = cv2.bitwise_not(img)
        text = pytesseract.image_to_string(img, lang='eng', config='--psm 10\
        --oem 3 -c tessedit_char_whitelist=0123456789')
        #img = cv2.resize(img, dst_size)
        cv2.imshow("test", img)
        print("Text: [" + text + "]")
        cv2.waitKey(1)

#get_text_from_screen_test()
#bug when trying to get gold from screen, exemple when trying to get 17 (11min20)
def text_finding():
    createTrackbar("LH", "win2", SHAPE_INFOS["l_b"][0], 255)
    createTrackbar("LS", "win2", SHAPE_INFOS["l_b"][1], 255)
    createTrackbar("LV", "win2", SHAPE_INFOS["l_b"][2], 255)
    
    createTrackbar("UH", "win2", SHAPE_INFOS["u_b"][0], 255)
    createTrackbar("US", "win2", SHAPE_INFOS["u_b"][1], 255)
    createTrackbar("UV", "win2", SHAPE_INFOS["u_b"][2], 255)
    
    frame = capture_screen(resize=1.5)
    while (True):
        frame = capture_screen(resize=1.5)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        l_h = cv2.getTrackbarPos("LH", "win2")
        l_s = cv2.getTrackbarPos("LS", "win2")
        l_v = cv2.getTrackbarPos("LV", "win2")
        
        u_h = cv2.getTrackbarPos("UH", "win2")
        u_s = cv2.getTrackbarPos("US", "win2")
        u_v = cv2.getTrackbarPos("UV", "win2")

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, l_b, u_b)
        res = cv2.bitwise_and(frame, frame, mask=mask)
       
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            obj_size_wanted = cv2.getTrackbarPos("obj_size", "win2")
            contour_area = cv2.contourArea(contour)
            if contour_area > (obj_size_wanted * 0.5) and contour_area < obj_size_wanted:
                cv2.rectangle(res, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()

#text_finding()

def test_capture():
    p1 = SHAPE_INFOS["point1_location_area"]
    p2 = SHAPE_INFOS["point2_location_area"]
    #frame = capture_screen(p1[0], p2[0], p1[1] - p1[0], p2[1] - p1[0])
    frame = capture_screen(p1[0], p1[1], p2[0], p2[1])
    cv2.imwrite('ressources\Test\capture_test_delme.png', frame)

#test_capture()