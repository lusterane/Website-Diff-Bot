import logging

import certifi
import urllib3
from urllib3 import exceptions as urllib3_exceptions

from Models import *


class Website_Scraper:
    def __init__(self):
        urllib3.disable_warnings()

    def scrape_request(self, request_object):
        try:
            raw_html = self.__get_raw_html_from_link(request_object.link)
            return ScrapingResponseObject(link=request_object.link,
                                          html_data=raw_html,
                                          email=request_object.email)
        except:
            return None

    def __get_raw_html_from_link(self, url):
        try:
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request('GET', url)
            return response.data.decode('utf-8')
        except urllib3_exceptions.MaxRetryError as e:
            print("Failed with: ", e)
            # try with insecure connection
            pass
        except Exception as e:
            print("Failed with: ", e)
            print("\nThrow Error ...")
            raise urllib3_exceptions.MaxRetryError
        try:
            print("\nWill try again with non-secure connection ...")
            http = urllib3.PoolManager(retries=0, cert_reqs='CERT_NONE')
            response = http.request('GET', url)
            return str(response.data.decode('utf-8'))
        except Exception as e:
            print("Failed with: ", e)
            print("\nThrow Error ...")
            raise urllib3_exceptions.MaxRetryError
