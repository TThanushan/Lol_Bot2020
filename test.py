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
main()