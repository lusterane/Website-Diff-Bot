import logging
import os

logger = logging.getLogger()

log_file_name = 'project-logs.txt'
log_file_path = f'logs/{log_file_name}'
logger.setLevel(logging.DEBUG)
# Create a file handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - line %(lineno)d in %(funcName)s() in %(filename)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# clear log file if too large
if os.path.exists(log_file_path):
    file_size = os.path.getsize(log_file_path)
    five_megabytes = 5000000
    if file_size > five_megabytes:
        try:
            with open(log_file_path, 'w') as f:
                f.truncate(0)
                logging.info(f"The file {log_file_name} has been cleared.")
        except OSError as e:
            logging.info(f"Error clearing the file {log_file_name}: {e.strerror}.")
