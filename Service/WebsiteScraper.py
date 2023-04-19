import inspect
import logging
import re

import certifi
import urllib3
from bs4 import BeautifulSoup
from urllib3 import exceptions as urllib3_exceptions

from Persistence.Models import *
from Service.Helper.ExceptionHelper import ExceptionHelper


class WebsiteScraper:
    def __init__(self):
        urllib3.disable_warnings()

    def scrape_link(self, link):
        logging.info(f'Starting Scraping {link}. . .')
        try:
            raw_html = self.__get_raw_html_from_link(link)
            logging.info('Scraping Success!')
            return raw_html
        except Exception as e:
            logging.info('Scraping Failed . . .')
            ExceptionHelper.raise_exception(str(e), inspect.currentframe().f_lineno, inspect.currentframe().f_code.co_name)

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
            ExceptionHelper.raise_exception(str(e), inspect.currentframe().f_lineno, inspect.currentframe().f_code.co_name)
        try:
            logging.info("Will try again with non-secure connection ...")
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_NONE')
            response = http.request('GET', url)
            raw_html_data = response.data.decode('utf-8')
            return self.__parse_with_beautiful_soup(raw_html_data)
        except Exception as e:
            ExceptionHelper.raise_exception(str(e), inspect.currentframe().f_lineno, inspect.currentframe().f_code.co_name)

    def __parse_with_beautiful_soup(self, raw_html_data):
        soup = BeautifulSoup(raw_html_data, 'html.parser')
        raw_content = soup.get_text()
        return self.__text_preprocessor(raw_content)

    def __text_preprocessor(self, raw_content):
        # general string preprocessing
        new_content = raw_content.strip()

        # replace multiple occurrences
        new_content = re.sub(' +', ' ', new_content)
        new_content = re.sub('\n+', '\n', new_content)

        # remove symbols
        # new_content = re.sub(r'[^\w\s]', ' ', new_content)

        # check if entire string is digit
        if new_content.isdigit():
            return ''

        # preprocess numbers with symbols
        for content in new_content.split(','):
            # if any ar e not numbers, then content is valid
            if not content.isdigit():
                return new_content
        return ''