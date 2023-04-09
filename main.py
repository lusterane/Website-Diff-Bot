import logging
import os.path

from DatabaseManager import DatabaseManager
from Models import RequestObject
from Website_Scraper import Website_Scraper

TESTING = False


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
    # initialize variables
    website_scraper = Website_Scraper()
    dm = DatabaseManager()
    request_objects = [RequestObject(email='tobychow98@gmail.com',
                                     link='https://www.sascassnime.ssscom/vendors-and-artists/artist-alley/artist-alley-registration/'),
                       RequestObject(email='daniel98@gmail.com',
                                     link='https://www.op.gg'),
                       RequestObject(email='joycezhao1@gmail.com',
                                     link='https://www.animeboston.com/artists/artists_alley/')]
    initialize_logger()

    logging.info('Starting Scraping . . .')
    # response htmls from requests
    response_object = website_scraper.scrape_request(request_objects[1])

    if not response_object:
        logging.info('Scraping Failed . . .')
        return
    logging.info('Scraping Success!')
    logging.info('Putting into DB . . .')
    # place into database
    if not dm.update_tables_with_scrape_response(response_object):
        logging.info('DB Querying Failed . . .')
        return

    logging.info('DB Querying Success!')


def testing_main():
    print('TESTING MAIN')

    # Email_Manager.test_email()


if __name__ == '__main__':
    if TESTING:
        testing_main()
    else:
        main()
