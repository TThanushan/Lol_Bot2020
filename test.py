"""Test"""
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
from image_functions import *
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# # 23, 66, 197, 35, 90, 255
# # 25, 65, 200, 65, 100, 255

# img = cv2.imread("ressources/test.png")
# img = apply_hsv_color_mask(img, 0, 0, 115, 50, 110, 255)
# img = cv2.bitwise_not(img)
# cv2.imshow("sa", img)
# cv2.waitKey(0)
# text = pytesseract.image_to_string(img)
# print(text)

while True:
    # img = capture_screen()
    # hide_image_outer_area([img], (1143, 1055), (1206, 1067))
    # # cv2.imshow("test", img)
    # # cv2.waitKey(0)
    # img = apply_hsv_color_mask(img, 0, 0, 115, 50, 110, 255)
    # img = cv2.bitwise_not(img)
    # text = pytesseract.image_to_string(img, lang='eng', config='--psm 10\
    #  --oem 3 -c tessedit_char_whitelist=0123456789')
    print(get_gold())


# def main2():
    
#     createTrackbar("LH", "win2", 0, 255)
#     createTrackbar("LS", "win2", 0, 255)
#     createTrackbar("LV", "win2", 0, 255)
    
#     createTrackbar("UH", "win2", 255, 255)
#     createTrackbar("US", "win2", 255, 255)
#     createTrackbar("UV", "win2", 255, 255)
    
#     frame = capture_screen(resize=2)
#     while (True):
#         frame = capture_screen(resize=2)
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

#         # cv2.imshow("frame", frame)
#         # cv2.imshow("mask", mask)
#         cv2.imshow("res", res)
#         if cv2.waitKey(40) == 27:
#             break
#     cv2.destroyAllWindows()
# main2()