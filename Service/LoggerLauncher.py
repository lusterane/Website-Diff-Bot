import logging
import os


class LoggerLauncher:
    @staticmethod
    def launch():
        # file handler initialization
        log_file_name = 'website-diff-logs.txt'
        log_file_path = f'logs/{log_file_name}'
        handler = logging.FileHandler(log_file_path)
        handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logging.getLogger().addHandler(handler)
        logging.getLogger().addHandler(console_handler)

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
