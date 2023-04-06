import certifi
import urllib3

class Website_Scraper:
    def get_raw_html_from_link(self, url):
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
