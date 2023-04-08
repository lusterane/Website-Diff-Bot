import pickle
from DatabaseManager import DatabaseManager
from Models import RequestObject
from Website_Scraper import Website_Scraper
import logging

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
    request_objects = [RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://www.sascassnime.ssscom/vendors-and-artists/artist-alley/artist-alley-registration/'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://animefest.org/e/AF2023/Activities/BizarreBazaar'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
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

    # save data locally
    # test_save_results_locally(encodedDictHTMLEntryModels)
    # encodedDictHTMLEntryModels = test_get_dict_from_local_results()
    # print(encodedDictHTMLEntryModels)


def test_save_results_locally(encodedDictHTMLEntryModels):
    count = 0
    for json_model in encodedDictHTMLEntryModels:
        with open(f"model_{str(count)}.json", 'wb') as write_file:
            pickle.dump(json_model, write_file, protocol=pickle.HIGHEST_PROTOCOL)
        count += 1


def test_get_dict_from_local_results():
    encodedDictHTMLEntryModels = []
    for count in range(3):
        with open(f"model_{str(count)}.json", 'rb') as read_file:
            encodedDictHTMLEntryModels.append(pickle.load(read_file))
    return encodedDictHTMLEntryModels


if __name__ == '__main__':
    main()
