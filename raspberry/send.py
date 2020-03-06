import socket
import sys
import random
from generate import *

HOST_IP = "127.0.0.1"
PORT = int(sys.argv[1])

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        rand = ['WIND', 'GUST', 'WIND', 'GUST', 'WIND']
        while True:
            try:
                s.connect((HOST_IP, PORT))
                break
            except Exception as e:
                print("trying socket connection..")
        data = s.recv(1024)
        a = str(data, encoding='ascii').split("\n")
        collect = []
        i = 0
        while i < 35:
            if a[0] == "OK":
                idx = random.randint(0,4)
                a = send_data(s, rand[idx])
                collect.append(a)
                i += 1
                if i % 5:
                    send_reset(s)
                    data = s.recv(1024)
                    a = str(data, encoding='ascii').split("\n")
            
            send_signal(s, "STOP")
        
        d = list(map(lambda c: str(c), collect))
        print("/".join(d))
