import re

import certifi
import urllib3
from bs4 import BeautifulSoup
from urllib3 import exceptions as urllib3_exceptions

from Services.LoggerContext import logger


class WebsiteScraper:
    @staticmethod
    def scrape_link(link):
        logger.info(f'Starting Scraping {link}. . .')
        urllib3.disable_warnings()
        try:
            raw_html = WebsiteScraper.__get_raw_html_from_link(link)
            logger.info('Scraping Success!')
            return raw_html
        except Exception as e:
            logger.critical('Scraping Failed . . .')
            raise e

    @staticmethod
    def __get_raw_html_from_link(link):
        try:
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request('GET', link)
            raw_html_data = response.data.decode('utf-8')
            return WebsiteScraper.__parse_with_beautiful_soup(raw_html_data)
        except urllib3_exceptions.MaxRetryError as e:
            logger.warning(f"Failed with: {e}")
            logger.warning("Will try again with non-secure connection ...")
            # try with insecure connection
            pass
        except Exception as e:
            raise e
        try:
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_NONE')
            response = http.request('GET', link)
            raw_html_data = response.data.decode('utf-8')
            return WebsiteScraper.__parse_with_beautiful_soup(raw_html_data)
        except Exception as e:
            raise e

    @staticmethod
    def __parse_with_beautiful_soup(raw_html_data):
        soup = BeautifulSoup(raw_html_data, 'html.parser')
        raw_content = soup.get_text()
        return WebsiteScraper.__text_preprocessor__(raw_content)

    @staticmethod
    def __text_preprocessor__(raw_content):
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
