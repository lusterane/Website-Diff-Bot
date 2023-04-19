import logging
import os.path

import Persistence.DBGateway as flask_app


def initialize_logger():
    # file handler initialization
    log_file_name = 'website-diff-logs.txt'

    handler = logging.FileHandler(log_file_name)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)

    # clear log file if too large
    if os.path.exists(log_file_name):
        file_size = os.path.getsize(log_file_name)
        half_megabyte = 500000
        if file_size > half_megabyte:
            try:
                with open(log_file_name, 'w') as f:
                    f.truncate(0)
                    logging.info(f"The file {log_file_name} has been cleared.")
            except OSError as e:
                logging.info(f"Error clearing the file {log_file_name}: {e.strerror}.")


def main():
    flask_app.app.run(debug=True)
    pass


if __name__ == '__main__':
    main()
