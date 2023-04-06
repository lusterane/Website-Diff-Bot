from Website_Scraper import Website_Scraper
from HTMLEntryObjectModel import HTMLEntryObjectModel, HTMLEntryObjectEncoder

if __name__ == '__main__':
    website_scraper = Website_Scraper()
    url1 = 'https://www.katsucon.org/katsucon-2023-artist-alley/'
    url2 = "https://animefest.org/e/AF2023/Activities/BizarreBazaar"
    url3 = "https://www.animeboston.com/artists/artists_alley/"
    urls = [url1,url2,url3]
    encodedDictHTMLEntryModels = []

    for url in urls:
        raw_html = website_scraper.get_raw_html_from_link(url)
        model = HTMLEntryObjectModel(customer="Joyce",html_data=raw_html,email="tobychow98@gmail.com")
        encodedDictHTMLEntryModels.append(HTMLEntryObjectEncoder().encode(model))
    print(encodedDictHTMLEntryModels)



