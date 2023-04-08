import pickle
from DatabaseManager import DatabaseManager
from Models import RequestObject
from Website_Scraper import Website_Scraper


def main():
    website_scraper = Website_Scraper()

    request_objects = [RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://www.sascassnime.ssscom/vendors-and-artists/artist-alley/artist-alley-registration/'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://animefest.org/e/AF2023/Activities/BizarreBazaar'),
                       RequestObject(name='Joyce', email='tobychow98@gmail.com',
                                     link='https://www.animeboston.com/artists/artists_alley/')]

    # response htmls from requests
    response_object = website_scraper.scrape_request(request_objects[0])

    if not response_object:
        return

    # place into database
    dm = DatabaseManager()
    dm.update_tables_with_scrape_response(response_object)

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
