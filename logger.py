import logging
#import inspect


class Logger(logging.getLoggerClass()):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, name_file, level=logging.DEBUG):
        logging.getLoggerClass().__init__(self, name=None)
        self.name_file = name_file
        self.handler = logging.StreamHandler()
        self.handler_file = logging.FileHandler(name_file)
        self.handler.setFormatter(self.formatter)
        self.addHandler(self.handler)
        self.setLevel(level)
        self.handler_file.setFormatter(self.formatter)
        self.addHandler(self.handler_file)


logger = Logger('test.log')
