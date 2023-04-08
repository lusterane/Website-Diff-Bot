import certifi
import urllib3

from Models import ScrapingResponseObject


class Website_Scraper:

    def scrape_requests(self, request_objects):
        response_objects = []
        for requestObject in request_objects:
            raw_html = self.__get_raw_html_from_link(requestObject.link)
            response_objects.append(ScrapingResponseObject(link=requestObject.link,
                                                           name=requestObject.name,
                                                           html_data=raw_html,
                                                           email=requestObject.email))
        return response_objects

    def __get_raw_html_from_link(self, url):
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request('GET', url)
            return response.data.decode('utf-8')
        except Exception as e:
            print("Failed with: ", e)
            print("\nWill try again with non-secure connection ...")
            http = urllib3.PoolManager(cert_reqs='CERT_NONE')
            response = http.request('GET', url)
            return str(response.data.decode('utf-8'))
