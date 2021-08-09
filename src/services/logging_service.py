import logging

default_formatter = '%(levelname)s - %(asctime)s - %(message)s'
default_formatter_datefmt = '%Y-%m-%d - %H:%M:%S'
default_file_handler = 'errors.log'


class LoggingService:
    def __init__(self, name, formatter=default_formatter, datefmt=default_formatter_datefmt, file_handler=default_file_handler):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter(formatter)
        self.formatter.datefmt = datefmt

        self.file_handler = logging.FileHandler(file_handler)
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(logging.ERROR)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.stream_handler.setLevel(logging.INFO)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def get_logger(self):
        return self.logger
