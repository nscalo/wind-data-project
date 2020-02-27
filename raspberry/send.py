import socket
import sys
import random

HOST_IP = "127.0.0.1"
PORT = int(sys.argv[1])

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("sending message")
        rand = ['WIND', 'GUST']
        s.connect((HOST_IP, PORT))
        data = s.recv(1024)
        a = str(data, encoding='ascii').split("\n")
        print("Received data", a)
        if a[0] == "OK":
            while True:
                idx = random.randint(0,1)
                s.send(bytes(rand[idx], encoding='ascii'))
                data = s.recv(1024)
                a = str(data, encoding='ascii').split("\n")
                print(a)
        
    print('Received', repr(data))