"""Test"""
from PIL import ImageGrab
import numpy as np
import cv2
from image_functions import *
# def capture_screen():
#     img = ImageGrab.grab(bbox=(0, 0, 1920, 1080)) #bbox specifies specific region (bbox= x,y,width,height)
#     img_np = np.array(img)
#     frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
#     return cv2.resize(frame, (round(1920/5), round(1080/5)))

def main():
    frame1 = capture_screen()
    frame2 = capture_screen()
    while (True):
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 250:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("inter", frame1)
        frame1 = frame2
        frame2 = capture_screen()
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()
def main2():
    
    createTrackbar("LH", "win2", 0, 255)
    createTrackbar("LS", "win2", 0, 255)
    createTrackbar("LV", "win2", 0, 255)
    
    createTrackbar("UH", "win2", 255, 255)
    createTrackbar("US", "win2", 255, 255)
    createTrackbar("UV", "win2", 255, 255)
    
    frame = capture_screen(resize=2)
    while (True):
        frame = capture_screen(resize=2)
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

        # cv2.imshow("frame", frame)
        # cv2.imshow("mask", mask)
        cv2.imshow("res", res)
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()
def main3():
    
    frame1 = capture_screen(resize=2)
    frame2 = capture_screen(resize=2)
    # frame1 = apply_hsv_color_mask(frame1, 103, 25, 90, 105, 240, 255)
    frame1 = apply_hsv_color_mask(frame1, 0, 100, 155, 15, 255, 255)
    createTrackbar("obj_size", "win2", 420, 3000)
    nb = 0
    while (True):
        frame2 = apply_hsv_color_mask(frame2, 0, 100, 155, 15, 255, 255)
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            obj_size_wanted = cv2.getTrackbarPos("obj_size", "win2")#420 for ally minions
            contour_area = cv2.contourArea(contour)
            if contour_area > obj_size_wanted and contour_area < obj_size_wanted * 1.7:
                nb += 1
                print(contour_area)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.imshow("frame", frame)
        # cv2.imshow("mask", mask)
        cv2.imshow("res", frame1)
        frame1 = frame2
        frame2 = capture_screen(resize=2)
        if cv2.waitKey(40) == 27:
            break
        print("nb :"+str(nb))
        nb = 0
    cv2.destroyAllWindows()

main3()
# To do
# Filter the image colors to see only wanted objects (ex: filter all colors except blue for ally minions)
def main4():
    createTrackbar("obj_size", "win2", 3000, 3000)
    frame1 = capture_screen(resize=2)
    frame2 = capture_screen(resize=2)
    while (True):
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            obj_size_wanted = cv2.getTrackbarPos("obj_size", "win2")
            contour_area = cv2.contourArea(contour)
            if contour_area > (obj_size_wanted * 0.5) and contour_area < obj_size_wanted:
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("inter", frame1)
        frame1 = frame2
        frame2 = capture_screen(resize=2)
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()