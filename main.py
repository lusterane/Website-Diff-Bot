from Website_Scraper import Website_Scraper
from Models import ScrapingResponseObject, HTMLEntryObjectEncoder, RequestObject
from DatabaseManager import DatabaseManager
from types import SimpleNamespace
import json
import pickle

def main():
    website_scraper = Website_Scraper()

    request_objects = [RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://www.katsucon.org/katsucon-2023-artist-alley/'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://animefest.org/e/AF2023/Activities/BizarreBazaar'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://www.animeboston.com/artists/artists_alley/')]

    # response htmls from requests
    response_objects = website_scraper.scrape_requests(request_objects)

    # place into database
    dm = DatabaseManager()
    dm.update_tables_with_response_objects(response_objects)

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
