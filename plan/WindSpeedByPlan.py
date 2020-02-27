import time, os, sys, socket, math, atexit
# import RPi.GPIO as GPIO
import raspberry.testGPIO as GPIO
from gpiozero import MCP3008
import time
try:
    import thread
except ImportError:
    import _thread as thread

RADIUS_CM = 9.0
WIND_SPEED_SENSOR_PIN = 5
BOUNCE_TIME = 1
HOST_IP = "127.0.0.1"
INERTIA = 2.0
SPEED_CALIBRATION_PARAMETER = 2.36
WIND_GUST_TIME = 5

class interrupt_watcher(object):

    def __init__(self, sensorPin, bounceTime, peak_sample = 5, peak_monitor = False):
        self.interrupt_count = 0
        self.running = True
        self.interrupt_peak_count = 0
        self.interrupt_peak_max = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(sensorPin, GPIO.FALLING, callback=self.interrupt_call_back, bouncetime=bounceTime)
        
        if peak_monitor:
            thread.start_new_thread(self.peak_monitor, (peak_sample,))
        
    def interrupt_call_back(self, channel):        
        self.interrupt_count += 1
        self.interrupt_peak_count += 1
    
    def get_value(self):
        return self.interrupt_count
        
    def get_peak(self):
        return self.interrupt_peak_max
        
    def reset_count(self):
        self.interrupt_count = 0
        self.interrupt_peak_count = 0
        self.interrupt_peak_max = 0
    
    def peak_monitor(self, sample_period):
        while self.running:
            time.sleep(sample_period)
            if self.interrupt_peak_count > self.interrupt_peak_max:
                self.interrupt_peak_max = self.interrupt_peak_count
            self.interrupt_peak_count = 0
        
    def __del__(self):
        self.running = False
        
class wind_speed_interrupt_watcher(interrupt_watcher):

    def __init__(self, radius_cm, sensorPin, bounceTime, calibration = SPEED_CALIBRATION_PARAMETER):
        super(wind_speed_interrupt_watcher, self).__init__(sensorPin, bounceTime, peak_sample = 5, peak_monitor = True)
        
        circumference_cm = (2 * math.pi) * radius_cm
        self.circumference = circumference_cm / 100000.0 #circumference in km
        self.calibration = calibration
        self.last_time = time.time()
        
    def calculate_speed(self, interrupt_count, interval_seconds):
        rotations = interrupt_count / INERTIA
        distance_per_second = (self.circumference * rotations) / interval_seconds
        speed_per_hour = distance_per_second * 3600
        return speed_per_hour * self.calibration
        
    def get_wind_speed(self):
        return self.calculate_speed(self.get_value(), time.time() - self.last_time)
        
    def get_wind_gust_speed(self):
        return self.calculate_speed(self.get_peak(), WIND_GUST_TIME) #5 seconds
        
    def reset_timer(self):
        self.last_time = time.time()

class wind_direction_interrupt_watcher(interrupt_watcher):

    def __init__(self):
        pass
    
    def setup(self):
        self.adc = MCP3008(channel=0)

    def get_average(self, angles):
        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

class interrupt_daemon(object):

    def __init__(self, port):
        self.running = False
        self.port = int(port)
        self.socket_data = "{0}\n"
        
    def setup(self):
        self.wind = wind_speed_interrupt_watcher(RADIUS_CM, WIND_SPEED_SENSOR_PIN, BOUNCE_TIME) #Maplin anemometer = radius of 9 cm, was 17 on prototype
        
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.bind((HOST_IP, self.port))
            self.running = True
        except Exception as e:
            raise e
            exit()
        
        self.skt.listen(10)
        print("Socket listening at ", HOST_IP, " at port : ", self.port)
        
    def send(self, conn, s):
        conn.sendall(self.socket_data.format(s).encode('utf-8'))
        
    def receive(self, conn, length):
        data = conn.recv(length)
        return data.decode('utf-8')
    
    def handle_connection(self, conn):
        connected = True
        self.send(conn, "OK")    
        
        while connected and self.running:
            data = self.receive(conn, 128)
            if len(data) > 0:
                data = data.strip()
                if data == "WIND":                    
                    self.send(conn, str(self.wind.get_wind_speed()))
                elif data == "GUST":
                    self.send(conn, str(self.wind.get_wind_gust_speed()))
                elif data == "RESET":
                    self.reset_counts()
                    self.send(conn, "OK")
                elif data == "BYE":
                    connected = False
                elif data == "STOP":
                    connected = False
                    self.stop()
                
        conn.close()
        
    def reset_counts(self):
        self.wind.reset_count()
        self.wind.reset_timer()
        
    def daemonize(self):
        # do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details (ISBN 0201563177)        
        # first fork
        try:
            self.pid = os.fork()
            if self.pid > 0:
                sys.exit(0)
        except OSError as e:
            print(e)
            raise
        
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)        
        
        # second fork
        try:
            self.pid = os.fork()
            if self.pid > 0:
                sys.exit(0)
        except OSError as e:
            print(e)
            raise
            
        # close file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
    def start(self, devices=1):
        try:
            self.daemon_pid = None
            self.daemonize()
            self.daemon_pid = os.getpid()
            print("PID: %d" % self.daemon_pid)
            self.setup()
            while self.running and devices == 1:
                conn, addr =  self.skt.accept() #blocking call
                self.handle_connection(conn)
        except Exception as e:
            raise e
            if self.running:
                self.stop()
        finally:
            if self.daemon_pid == os.getpid():
                self.skt.shutdown(socket.SHUT_RDWR)
                self.skt.close()
                GPIO.cleanup()
                print("Stopped")
        
    def stop(self):
        self.running = False        
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("localhost", self.port)) #release blocking call
