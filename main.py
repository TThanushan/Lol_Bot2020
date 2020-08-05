"""Main file"""
import threading
import time
import cv2
import bot
import application_window as app_win
from window_capture import windowCapture
import game_data
import image_functions as img_func

Bot = bot.Bot()
GameData = game_data.GameData()

def main():
    t_app = threading.Thread(target=app_win.create_app_win(Bot.GameData))
    # thread_1 = threading.Thread(target=crucial_thread)
    # thread_2 = threading.Thread(target=normal_thread)

    t_app.start()
    # thread_1.start()
    # thread_2.start()

# main()



# wincap = window_capture.WindowCapture('*Untitled - Notepad')
# GameData = game_data.GameData()
loop_time = time.time()


ALLIED_MINIONS_INFOS = {
    "min_size" : 125,
    "max_size" : 500,
    "l_b" : [0, 135, 110],
    "u_b" : [0, 140, 205]
    }

def get_shapes_contours(shapes_hsv_bound, frame):
    # frame = capture_screen(resize=1.5)
    res =  img_func.apply_hsv_color_mask(frame, shapes_hsv_bound)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_shapes_pos(shapes_hsv, frame):
    positions = []
    contours = get_shapes_contours(shapes_hsv, frame)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > shapes_hsv["min_size"] and contour_area < shapes_hsv["max_size"]:
            (x, y, w, h) = cv2.boundingRect(contour)
            positions.append([round(x+w/2), round(y)])
    return positions

def draw_contour(img, contours):
    if len(contours) == 0:
        return
    for contour in contours:
        cv2.circle(img, tuple(contour), 4, (0, 255, 0))
while True:
    screenshot = windowCapture.get_new_screenshot()
    all_pos = get_shapes_pos(ALLIED_MINIONS_INFOS, screenshot)
    draw_contour(screenshot, all_pos)
    cv2.imshow('Computer Vision', screenshot)

    if time.time() - loop_time != 0:
        print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
print('done')


