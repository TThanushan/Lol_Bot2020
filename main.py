"""Main file"""
import cv2
import Bot as botmod
import threading
import time
import image_functions
from bot_functions import *
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

def create_app_win():
    win = cv2.namedWindow("Wombot")
    # createTrackbar("pt1x", "Wombot", 0, 1000)
    # createTrackbar("pt1y", "Wombot", 0, 1000)
    # createTrackbar("pt2x", "Wombot", 0, 1000)
    # createTrackbar("pt2y", "Wombot", 0, 1000)
    while True:

        # pt1x = cv2.getTrackbarPos("pt1x", "Wombot")
        # pt1y = cv2.getTrackbarPos("pt1y", "Wombot")
        # pt2x = cv2.getTrackbarPos("pt2x", "Wombot")
        # pt2y = cv2.getTrackbarPos("pt2y", "Wombot")
        # pt1 = (pt1x, pt1y)
        # pt2 = (pt2x, pt2y)
        img = cv2.imread("ressources/gui/gui_bg.png")
        color = (0, 0, 255)
        # cv2.rectangle(img, pt1, pt2, color, 6)
        # low_life
        color = change_color(bot.screen_infos.low_life)
        cv2.rectangle(img, (250, 35), (507, 127), color, 6)
        # a_minions
        color = change_color(bot.screen_infos.ally_minions)
        cv2.rectangle(img, (58, 188), (180, 310), color, 6)
        # e_minions
        color = change_color(bot.screen_infos.enemy_minions)
        cv2.rectangle(img, (230, 190), (358, 310), color, 6)
        # a_champions
        color = change_color(bot.screen_infos.ally_minions)
        cv2.rectangle(img, (408, 190), (535, 310), color, 6)
        # e_champions
        color = change_color(bot.screen_infos.enemy_champions)
        cv2.rectangle(img, (590, 190), (722, 310), color, 6)

        # at_fountain
        color = change_color(bot.screen_infos.at_fountain)
        cv2.rectangle(img, (20, 47), (210, 150), color, 6)
        
        # gold
        img = cv2.putText(img, str(bot.screen_infos.gold), (620, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (210, 255, 255), 2)
        
        # Action
        img = cv2.putText(img, bot.action, (300, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        img = cv2.resize(img, (500, 425), interpolation=cv2.INTER_AREA)
        cv2.imshow("Wombot", img)
        # cv2.resizeWindow("Wombot", 500, 500)
        cv2.waitKey(1)

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
#main()
#create_app_win()
# print(image_functions.is_at_fountain())
#while True:
#    print('ally minions nb: ' + str(get_ally_minion_nb()))
    #print('enemy minions nb: ' + str(get_enemy_minion_nb()))
