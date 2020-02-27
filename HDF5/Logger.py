import logging

class Logger():

    def __init__(self, speed='speed.log', direction='direction.log'):
        logging.basicConfig(level=logging.DEBUG)
        self.speed_logger = logging.getLogger('speed_logger')
        self.direction_logger = logging.getLogger('direction_logger')
        log_format = logging.Formatter('%(asctime)s \t %(name)s \t\t %(levelname)s \t %(message)s')
        speed_handler = logging.FileHandler(speed)
        direction_handler = logging.FileHandler(direction)
        speed_handler.setFormatter(log_format)
        direction_handler.setFormatter(log_format)
        self.speed_logger.addHandler(speed_handler)
        self.direction_logger.addHandler(direction_handler)

    def log(self, name, level, message):
        if name == "speed":
            getattr(self.speed_logger, level)(message)
        elif name == "direction":
            getattr(self.direction_logger, level)(message)
    
