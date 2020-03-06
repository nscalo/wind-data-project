import socket
import sys
from plan.WindSpeed import *

HOST_IP = "127.0.0.1"
PORT = sys.argv[1]

if __name__ == "__main__":

    daemon = interrupt_daemon(sys.argv[1])
    daemon.start()
    
