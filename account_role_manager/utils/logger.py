import logging
import os
from datetime import datetime

class Logger:
    _instances = {}

    def __new__(cls, name: str, log_dir: str = 'logs', log_level: int = logging.INFO):
        # Singleton pattern to ensure only one instance per logger name
        if name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            instance._initialize(name, log_dir, log_level)
            cls._instances[name] = instance
        return cls._instances[name]

    def _initialize(self, name: str, log_dir: str, log_level: int):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Check if the logger already has handlers to avoid duplicate logs
        if not self.logger.handlers:
            # Create the log directory if it doesn't exist
            log_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), log_dir)
            os.makedirs(log_dir_path, exist_ok=True)

            # Define the log file format
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            log_file = os.path.join(log_dir_path, f'app_{datetime.now().strftime("%Y%m%d")}.log')

            # Create a file handler to write logs to the file
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(file_formatter)

            # Add the file handler to the logger
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        # Return the configured logger instance
        return self.logger