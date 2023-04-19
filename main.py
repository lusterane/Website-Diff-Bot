import logging
import os.path

import Presentation.FlaskAPIRouting as flask_app
from Persistence.Models import RequestObject
from Service.DatabaseManager import DatabaseManager
from Service.WebsiteScraper import WebsiteScraper

TESTING = os.environ.get("TESTING")


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
    website_scraper = WebsiteScraper()
    dm = DatabaseManager()
    initialize_logger()

    res = website_scraper.scrape_link('https://www.animeboston.com/artists/artists_alley/')
    print(res)
    # response htmls from requests
    # response_object = website_scraper.scrape_link(request_objects[1])
    #
    # if not response_object:
    #     return
    # logging.info('Scraping Success!')
    # logging.info('Putting into DB . . .')
    # # place into database
    # if not dm.update_tables_with_scrape_response(response_object):
    #     logging.info('DB Querying Failed . . .')
    #     return
    #
    # logging.info('DB Querying Success!')


def testing_main():
    print('TESTING MAIN')
    flask_app.app.run(debug=True)
    # Email_Manager.test_email()


if __name__ == '__main__':
    if TESTING == '1':
        testing_main()
    else:
        main()
