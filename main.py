"""Main file"""
import cv2
import Bot as botmod
import threading
import time
import image_functions
from bot_functions import *
import sys
bot = botmod.Bot()
def createTrackbar(name, win_name, value, count):
    def nothing(x):
        x += 0
    cv2.namedWindow(win_name)
    cv2.createTrackbar(name, win_name, value, count, nothing)    

def change_color(bool_v):
    if bool_v:
        return (0, 255, 0)
    return (0, 0, 255)

COLORS = {
    "White" : [255, 255, 255],
    "Red" : [255, 42, 0],
    "Green" : [130, 245, 157],
    "Yellow" : [255, 213, 0],
    "Blue" : [3, 190, 252],
    "Cyan" : [148, 228, 255],
    "Orange" : [255, 213, 0],
    }
TEXT_COLORS = [COLORS["Green"],
               COLORS["Blue"],
               COLORS["White"],
               COLORS["Cyan"],
               COLORS["Orange"],
               COLORS["Red"],
               COLORS["Orange"],
               COLORS["Green"],
               COLORS["Yellow"],
               ]
def RGB2BGR(color):
    return (color[2], color[1], color[0])
def display_all_screen_infos(img):
    x_text_pos = 50
    y_text_pos = 70
    y_spacing = 50
    all_infos = bot.screen_infos.get_all_properties()
    color_index = 0
    for attr in all_infos:
        img = cv2.putText(img, attr + ': ' + str(all_infos[attr]), (x_text_pos, y_text_pos),\
            cv2.FONT_HERSHEY_SIMPLEX, 1, RGB2BGR(TEXT_COLORS[color_index]), 2)
        y_text_pos = y_text_pos + y_spacing
        color_index = color_index + 1

def create_app_win():
    win = cv2.namedWindow("Wombot")
    img = cv2.imread("ressources/gui/background.png")
    while bot.running:
        img = cv2.imread("ressources/gui/background.png")
        display_all_screen_infos(img)
        img = cv2.resize(img, (500, 425), interpolation=cv2.INTER_AREA)
        cv2.imshow("Wombot", img)
        key_pressed = cv2.waitKey(1)
        if str(key_pressed) == '27':
            bot.running = False
    cv2.destroyAllWindows()

def main():
    t_app = threading.Thread(target=create_app_win)
    t1 = threading.Thread(target=bot.fast_thread)
    t2 = threading.Thread(target=bot.middle_thread)
    t3 = threading.Thread(target=bot.slow_thread)
    #t4 = threading.Thread(target=bot.behavior_loop)
    t_app.start()

    t1.start()
    t2.start()
    t3.start()

    #t4.start()
# time.sleep(2)
# bot.do_once()
#create_app_win()
# print(image_functions.is_at_fountain())

main()


#@utils.check_exec_time()
#def speed_test():
#    print(str(get_current_mana()))

#def test():
#    while True:
#        speed_test()
#test()
