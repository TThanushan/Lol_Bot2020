# directkeys.py
# http://stackoverflow.com/questions/13564851/generate-keyboard-events
# msdn.microsoft.com/en-us/library/dd375731

import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731
UP = 0x26
DOWN = 0x28
A = 0x41

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize


CHAR_TO_HEXKEYCODE = {
    'a' : 0x41,
    'b' : 0x42,
    'c' : 0x43,
    'd' : 0x44,
    'e' : 0x45,
    'f' : 0x46,
    'g' : 0x47,
    'h' : 0x48,
    'i' : 0x49,
    'j' : 0x4A,
    'k' : 0x4B,
    'l' : 0x4C,
    'm' : 0x4D,
    'n' : 0x4E,
    'o' : 0x4F,
    'p' : 0x50,
    'q' : 0x51,
    'r' : 0x52,
    's' : 0x53,
    't' : 0x54,
    'u' : 0x55,
    'v' : 0x56,
    'w' : 0x57,
    'x' : 0x58,
    'y' : 0x59,
    'z' : 0x5A
}

# Functions
def PressKey(char_key):
    hex_keycode = CHAR_TO_HEXKEYCODE[char_key]
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hex_keycode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    ReleaseKey(char_key)
def ReleaseKey(char_key):
    hex_keycode = CHAR_TO_HEXKEYCODE[char_key]
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hex_keycode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def MaintainKey(char_key):
    hex_keycode = CHAR_TO_HEXKEYCODE[char_key]
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hex_keycode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

MOUSE_LEFTDOWN = 0x0002     # left button down 
MOUSE_LEFTUP = 0x0004       # left button up 
MOUSE_RIGHTDOWN = 0x0008    # right button down 
MOUSE_RIGHTUP = 0x0010      # right button up 
MOUSE_MIDDLEDOWN = 0x0020   # middle button down 
MOUSE_MIDDLEUP = 0x0040     # middle button up 

def pos(x, y):
    ctypes.windll.user32.SetCursorPoas(x, y)

def click(button_down, button_up):
    ctypes.windll.user32.mouse_event(button_down, 0, 0, 0,0) # left down
    ctypes.windll.user32.mouse_event(button_up, 0, 0, 0,0) # left up

def mouse_left_click():
    click(MOUSE_LEFTDOWN, MOUSE_LEFTUP)

def mouse_right_click():
    click(MOUSE_RIGHTDOWN, MOUSE_RIGHTUP)

def mouse_middle_click():
    click(MOUSE_MIDDLEDOWN, MOUSE_MIDDLEUP)
