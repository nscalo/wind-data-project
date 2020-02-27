#!/usr/bin/python
BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
FALLING = 1
PUD_UP = "up"
 
def output(pin,value):
  print(pin, ":", value)
 
def setmode(mode):
  print(mode) 
def setup(pin,value,pull_up_down=None):
  print(pin, ":", value, ":", pull_up_down)
 
def cleanup():
  print("clean-up")

def add_event_detect(sensorPin, mode, callback=None, bouncetime=0.01):
  print(sensorPin, mode)
 
#End