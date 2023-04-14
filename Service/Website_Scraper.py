import logging
import re
import certifi
import urllib3
from urllib3 import exceptions as urllib3_exceptions
from bs4 import BeautifulSoup
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
            raw_html_data = response.data.decode('utf-8')
            return self.__parse_with_beautiful_soup(raw_html_data)
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
            raw_html_data = response.data.decode('utf-8')
            return self.__parse_with_beautiful_soup(raw_html_data)
        except Exception as e:
            logging.info(f"Failed with: {e}")
            raise e

    def __parse_with_beautiful_soup(self, raw_html_data):
        soup = BeautifulSoup(raw_html_data, 'html.parser')
        content = ''
        for tag in soup.find_all():
            raw_content = tag.text

            # preprocessing
            processed_content = self.__text_preprocessor(raw_content)

            if not processed_content:
                continue
            content += processed_content
        return content

    def __text_preprocessor(self, raw_content):
        # general string preprocessing
        new_content = raw_content.strip()
        new_content = re.sub(r'\n+', r'\n', new_content)

        # check if entire string is digit
        if new_content.isdigit():
            return ''

        # preprocess numbers with symbols
        for content in new_content.split(','):
            # if any are not numbers, then content is valid
            if not content.isdigit():
                return new_content
        return ''
