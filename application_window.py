import cv2

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

def createTrackbar(name, win_name, value, count):
    cv2.namedWindow(win_name)
    cv2.createTrackbar(name, win_name, value, count)

def RGB2BGR(color):
    return (color[2], color[1], color[0])

def display_all_screen_infos(img, GameData):
    x_text_pos = 50
    y_text_pos = 70
    y_spacing = 50
    all_infos = GameData.get_all_properties()
    color_index = 0
    for attr in all_infos:
        img = cv2.putText(img, attr + ': ' + str(all_infos[attr]), (x_text_pos, y_text_pos),\
            cv2.FONT_HERSHEY_SIMPLEX, 1, RGB2BGR(TEXT_COLORS[color_index]), 2)
        y_text_pos = y_text_pos + y_spacing
        color_index = color_index + 1

def create_app_win(GameData):
    img = cv2.imread("ressources/gui/background.png")
    while True:
        img = cv2.imread("ressources/gui/background.png")
        display_all_screen_infos(img, GameData)
        img = cv2.resize(img, (500, 425), interpolation=cv2.INTER_AREA)
        cv2.imshow("Wombot", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
