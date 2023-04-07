import certifi
import urllib3
from Models import HTMLEntryObjectModel, HTMLEntryObjectEncoder, RequestObject

class Website_Scraper:

    def get_encoded_dict_HTML_Entries(self,requestObjects):
        encodedDictHTMLEntryModels = []
        for requestObject in requestObjects:
            raw_html = self.__get_raw_html_from_link(requestObject.link)
            model = HTMLEntryObjectModel(customer=requestObject.user, html_data=raw_html, email=requestObject.email)
            encodedDictHTMLEntryModels.append(HTMLEntryObjectEncoder().encode(model))
        return encodedDictHTMLEntryModels
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
