import logging

from DatabaseManager import DatabaseManager
from Models import RequestObject
from Website_Scraper import Website_Scraper


def initialize_logger():
    handler = logging.FileHandler('Website-Diff-Bot Logger')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)


def main():
    # initialize variables
    website_scraper = Website_Scraper()
    dm = DatabaseManager()
    request_objects = [RequestObject(email='tobychow98@gmail.com',
                                     link='https://www.sascassnime.ssscom/vendors-and-artists/artist-alley/artist-alley-registration/'),
                       RequestObject(email='tobychow98@gmail.com',
                                     link='https://animefest.org/e/AF2023/Activities/BizarreBazaar'),
                       RequestObject(email='joycezhao1@gmail.com',
                                     link='https://www.animeboston.com/artists/artists_alley/')]
    initialize_logger()

    logging.info('Starting Scraping . . .')
    # response htmls from requests
    response_object = website_scraper.scrape_request(request_objects[0])

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


if __name__ == '__main__':
    main()
