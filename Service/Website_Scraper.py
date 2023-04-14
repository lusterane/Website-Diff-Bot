import logging

import certifi
import urllib3
from urllib3 import exceptions as urllib3_exceptions

from Persistence.Models import *


class Website_Scraper:
    def __init__(self):
        urllib3.disable_warnings()

    def scrape_request(self, request_object):
        logging.info(f'Starting Scraping {request_object.link} for {request_object.email}. . .')
        try:
            raw_html = self.__get_raw_html_from_link(request_object.link)
            logging.info('Scraping Success!')
            return ScrapingResponseObject(link=request_object.link,
                                          html_data=raw_html,
                                          email=request_object.email)
        except Exception as e:
            logging.info('Scraping Failed . . .')
            raise e

    def __get_raw_html_from_link(self, url):
        try:
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request('GET', url)
            return response.data.decode('utf-8')
        except urllib3_exceptions.MaxRetryError as e:
            logging.info(f"Failed with: {e}")
            # try with insecure connection
            pass
        except Exception as e:
            logging.info(f"Failed with: {e}")
            raise e
        try:
            logging.info("Will try again with non-secure connection ...")
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_NONE')
            response = http.request('GET', url)
            return str(response.data.decode('utf-8'))
        except Exception as e:
            logging.info(f"Failed with: {e}")
            raise e
