import logging
import os

from flask import Flask

from Service.Database_Manager import DatabaseManager
from Service.Website_Scraper import Website_Scraper


class Flask_Initialization_Service:
    def __init__(self):
        self.app = Flask(__name__)

        self.__initialize_logger()
        self.website_scraper = Website_Scraper()
        self.dm = DatabaseManager()

    def __initialize_logger(self, ):
        # file handler initialization
        log_file_name = 'website-diff-logs.txt'
        log_file_path = f'../logs/{log_file_name}'
        handler = logging.FileHandler(log_file_path)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logging.getLogger().addHandler(handler)

        # clear log file if too large
        if os.path.exists(log_file_path):
            file_size = os.path.getsize(log_file_path)
            half_megabyte = 500000
            if file_size > half_megabyte:
                try:
                    with open(log_file_path, 'w') as f:
                        f.truncate(0)
                        logging.info(f"The file {log_file_name} has been cleared.")
                except OSError as e:
                    logging.info(f"Error clearing the file {log_file_name}: {e.strerror}.")
