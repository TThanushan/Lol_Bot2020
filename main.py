"""Main file"""
import time
import directkeys as dk
import Bot as botmod
import pynput
import ctypes
import random

time.sleep(2)
bot = botmod.Bot()
bot.buy_item("doran's shield")
bot.buy_item("health potion")
bot.buy_item("warding totem")
