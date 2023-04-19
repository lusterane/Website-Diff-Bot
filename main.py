import logging
import os.path
from datetime import datetime

from Persistence.DBGateway import *


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
    current_time = datetime.datetime.now()
    job_data = {
        'j_id': None,
        'job_name': 'UPDATED test job name',
        'link': 'https://google.com/',
        'frequency': '100',
        'last_updated': current_time,
        'next_update': current_time,
        'p_id': '1',
        's_id': '1',
        'up_id': '1'
    }
    print(Profile.create_profile('tobychow98@gmail.com'))
    print(ScrapedData.create_scraped_data('this is test scraped data'))
    print(Update.create_update('this is test update'))
    print(Job.create_job(job_data))
    print(Job.get_job_by_id(2))
    pass


if __name__ == '__main__':
    main()
