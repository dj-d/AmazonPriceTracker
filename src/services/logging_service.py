import logging

default_formatter = '%(levelname)s - %(asctime)s - %(message)s'
default_formatter_datefmt = '%Y-%m-%d - %H:%M:%S'

default_file_handler = 'errors.log'


class LoggingService:
    def __init__(self, name, formatter, datefmt, file_handler):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if formatter is None:
            selected_formatter = default_formatter
        else:
            selected_formatter = formatter

        self.formatter = logging.Formatter(selected_formatter)

        if datefmt is None:
            selected_datefmt = default_formatter_datefmt
        else:
            selected_datefmt = datefmt

        self.formatter.datefmt = selected_datefmt

        if file_handler is None:
            selected_file_handler = default_file_handler
        else:
            selected_file_handler = file_handler

        self.file_handler = logging.FileHandler(selected_file_handler)
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(logging.ERROR)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.stream_handler.setLevel(logging.INFO)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def get_logger(self):
        return self.logger
