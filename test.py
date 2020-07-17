"""Test"""
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import directkeys as dk
from image_functions import *
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# # 23, 66, 197, 35, 90, 255
# # 25, 65, 200, 65, 100, 255

# img = cv2.imread("ressources/Test/Screenshot_9.png")
# # img = apply_hsv_color_mask(img, 0, 0, 115, 50, 110, 255)
# # img = apply_hsv_color_mask(img, 26, 23, 139, 35, 146, 255)
# # img = cv2.bitwise_not(img)
# # img = cv2.resize(img, (500, 500))
# cv2.imshow("sa", img)
# cv2.waitKey(0) 
# text = pytesseract.image_to_string(img, lang='eng', config='--psm 10\
#     --oem 3 -c tessedit_char_whitelist=0123456789')
# print(text)
# while True:
#     img = capture_screen()
#     hide_image_outer_area([img], (1143, 1055), (1206, 1070))
    
#     img = apply_hsv_color_mask(img, 0, 50, 75, 255, 255, 255)
#     img = cv2.resize(img, (round(1920*1.5), round(1080*1.5)))
#     img = cv2.bitwise_not(img)
#     text = pytesseract.image_to_string(img, lang='eng', config='--psm 10\
#      --oem 3 -c tessedit_char_whitelist=0123456789')
#     img = cv2.resize(img, (round(1920/2), round(1080/2)))
#     cv2.imshow("test", img)
#     cv2.waitKey(1)
#     print(text)

#bug when trying to get gold from screen, exemple when trying to get 17 (11min20)
# def main2():
#     createTrackbar("LH", "win2", 100, 255)
#     createTrackbar("LS", "win2", 125, 255)
#     createTrackbar("LV", "win2", 130, 255)
    
#     createTrackbar("UH", "win2", 105, 255)
#     createTrackbar("US", "win2", 185, 255)
#     createTrackbar("UV", "win2", 190, 255)
#     createTrackbar("obj_size", "win2", 420, 1000)
    
#     frame = capture_screen(resize=1.5)
#     while (True):
#         frame = capture_screen(resize=1.5)
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         l_h = cv2.getTrackbarPos("LH", "win2")
#         l_s = cv2.getTrackbarPos("LS", "win2")
#         l_v = cv2.getTrackbarPos("LV", "win2")
        
#         u_h = cv2.getTrackbarPos("UH", "win2")
#         u_s = cv2.getTrackbarPos("US", "win2")
#         u_v = cv2.getTrackbarPos("UV", "win2")

#         l_b = np.array([l_h, l_s, l_v])
#         u_b = np.array([u_h, u_s, u_v])
#         mask = cv2.inRange(hsv, l_b, u_b)
#         res = cv2.bitwise_and(frame, frame, mask=mask)
       
#         gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (5, 5), 0)
#         _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#         dilated = cv2.dilate(thresh, None, iterations=3)
#         contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         for contour in contours:
#             (x, y, w, h) = cv2.boundingRect(contour)
#             obj_size_wanted = cv2.getTrackbarPos("obj_size", "win2")
#             contour_area = cv2.contourArea(contour)
#             if contour_area > (obj_size_wanted * 0.5) and contour_area < obj_size_wanted:
#                 cv2.rectangle(res, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.imshow("frame", frame)
#         cv2.imshow("mask", mask)
#         cv2.imshow("res", res)
#         if cv2.waitKey(40) == 27:
#             break
#     cv2.destroyAllWindows()
def main3():
    createTrackbar("LH", "win2", 0, 255)
    createTrackbar("LS", "win2", 105, 255)
    createTrackbar("LV", "win2", 95, 255)
    
    createTrackbar("UH", "win2", 5, 255)
    createTrackbar("US", "win2", 160, 255)
    createTrackbar("UV", "win2", 195, 255)
    createTrackbar("obj_size", "win2", 440, 1000)
    # createTrackbar("x1", "win2", 240, 2000)
    # createTrackbar("y1", "win2", 80, 2000)
    # createTrackbar("x2", "win2", 960, 2000)
    # createTrackbar("y2", "win2", 560, 2000)
    
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
        # pt1 = (cv2.getTrackbarPos("x1", "win2"), cv2.getTrackbarPos("y1", "win2"))
        # pt2 = (cv2.getTrackbarPos("x2", "win2"), cv2.getTrackbarPos("y2", "win2"))
        hide_image_outer_area([frame, mask, res], (240, 80), (960, 560))
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        nb = 0
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            obj_size_wanted = cv2.getTrackbarPos("obj_size", "win2")
            contour_area = cv2.contourArea(contour)
            if contour_area > (obj_size_wanted * 0.25) and contour_area < obj_size_wanted:
                # nb += 1
                cv2.circle(frame, (round(x+w/2), round(y+40)), 3, (0, 0, 255))
                print(str((round((x*1.5)+40), round((y*1.5)+60))))
                cv2.rectangle(res, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # print(str(nb))
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)
        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()


# def get_minion_nb(obj_size_wanted, l_b, u_b):
#     frame = capture_screen(resize=1.5)
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, np.array(l_b), np.array(u_b))
#     res = cv2.bitwise_and(frame, frame, mask=mask)
#     hide_image_outer_area([res], (240, 80), (960, 560))
#     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#     dilated = cv2.dilate(thresh, None, iterations=3)
#     contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     occurence = 0
#     for contour in contours:
#         obj_size = obj_size_wanted
#         contour_area = cv2.contourArea(contour)
#         if (obj_size / 2) < contour_area < obj_size:
#             occurence += 1
#     return occurence
# def get_a_minion_nb():
#     return get_minion_nb(420, [100, 125, 130], [105, 185, 190])
# def get_e_minion_nb():
#     return get_minion_nb(640, [100, 125, 130], [105, 185, 190])
# main3()

# pos = get_e_minion_pos()
# print(str(pos))
# for p in pos:
#     dk.mouse_pos(p[0], p[1])
#     time.sleep(1)
E_MINIONS_HSV = {
    "size" : 640,
    "l_b" : [0, 115, 130],
    "u_b" : [4, 150, 195]
    }
pos = get_minions_position(E_MINIONS_HSV["size"], E_MINIONS_HSV["l_b"],\
             E_MINIONS_HSV["u_b"])
print(str(get_minions_position(E_MINIONS_HSV["size"], E_MINIONS_HSV["l_b"],\
             E_MINIONS_HSV["u_b"])))
