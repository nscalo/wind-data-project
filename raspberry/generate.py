import socket
import sys
import random

HOST_IP = "127.0.0.1"

def initiate_communication(PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST_IP, PORT))
    data = s.recv(1024)
    a = str(data, encoding='ascii').split("\n")
    if a[0] == "OK":
        return True, s
    return False, None

def send_reset(s):
    data = "RESET"
    s.send(bytes(data, encoding='ascii'))
    data = s.recv(1024)
    a = str(data, encoding='ascii').split("\n")
    return a[0]

def send_data(s, data):
    s.send(bytes(data, encoding='ascii'))
    data = s.recv(1024)
    a = str(data, encoding='ascii').split("\n")
    return float(a[0])

def send_signal(s, data):
    s.send(bytes(data, encoding='ascii'))
    return None