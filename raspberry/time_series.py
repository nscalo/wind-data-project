import numpy as np
from raspberry.generate import send_reset, initiate_communication
import mpi4py

SECONDS = 3600
HOURS = 24
TOTAL_FOR = 30 # days

def wind_percentage():
    return [0.6, 0.4]

class Cron():

    def __init__(self):
        self.init()

    def init(self):
        ok, s = initiate_communication()
        if ok == True:
            self.s = s
        else:
            self.s = None
            raise Exception("Socket connection could not be made")

    def reset_cron(self, period=5):
        while self.s is not None:
            send_reset(self.s)
        else:
            self.init()
    
def wind_gen(n, pvals=wind_percentage(), size=2):
    return np.random.multinomial(n, pvals, size)
