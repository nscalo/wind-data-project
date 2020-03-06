#!/usr/bin/python

from time_series import *
from time import time, sleep
from threading import Thread

BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
FALLING = 1
PUD_UP = "up"

SIMULATOR_RUNTIME = 30 # 30 seconds
NUMBER_ROWS = 21 + 14 # 21 wind signals and 14 gust signals

def output(pin,value):
  print(pin, ":", value)
 
def setmode(mode):
  print(mode) 
def setup(pin,value,pull_up_down=None):
  print(pin, ":", value, ":", pull_up_down)
 
def cleanup():
  print("clean-up")

def add_event_detect(sensorPin, mode, callback=None, bouncetime=0.01):
  bounceTime = 1.0 / 7.0 # seconds per reading
  idx = 0
  while idx < 300:
    sleep(bounceTime)
    callback(None)
    idx += 1
  print("finished detection stage..")
