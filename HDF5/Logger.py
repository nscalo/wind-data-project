import logging

class Logger():

    def __init__(self, speed=None, direction=None):
        logging.basicConfig(level=logging.DEBUG)
        log_format = logging.Formatter('%(asctime)s \t %(name)s \t\t %(levelname)s \t %(message)s')
        if speed is not None:
            self.setup_speed(speed, log_format)
        if direction is not None:
            self.setup_direction(direction, log_format)

    def setup_speed(self, speed, log_format):
        self.speed_logger = logging.getLogger('speed_logger')
        speed_handler = logging.FileHandler(speed)
        speed_handler.setFormatter(log_format)
        self.speed_logger.addHandler(speed_handler)
    
    def setup_direction(self, direction, log_format):
        self.direction_logger = logging.getLogger('direction_logger')
        direction_handler = logging.FileHandler(direction)
        direction_handler.setFormatter(log_format)
        self.direction_logger.addHandler(direction_handler)

    def log(self, name, level, message):
        if name == "speed":
            getattr(self.speed_logger, level)(message)
        elif name == "direction":
            getattr(self.direction_logger, level)(message)
    
