from json import JSONEncoder

'''
Users:
pk, email, name, link_pk

HTML_DATA_TABLE:
pk, link, html_data

'''


class ScrapingResponseObject:
    def __init__(self, link, name, html_data, email):
        self.link = link
        self.name = name
        self.html_data = html_data
        self.email = email

    def __repr__(self):
        return f'Link: {self.link}\nEmail: {self.email}\nName: {self.name}\nHtml Data:\n{self.html_data}\n'


class RequestObject:
    def __init__(self, name, email, link):
        self.name = name
        self.email = email
        self.link = link


class DBHTMLEntryObject:
    def __init__(self, html_data_id, link, html_data):
        self.html_data_id = html_data_id
        self.link = link
        self.html_data = html_data


class DBUserEntryObject:
    def __init__(self, user_data_id, email, name, html_data_fk):
        self.user_data_id = user_data_id
        self.email = email
        self.name = name
        self.html_data_fk = html_data_fk


class HTMLEntryObjectEncoder(JSONEncoder):
    def default(self, o: ScrapingResponseObject) -> ScrapingResponseObject:
        return o.__dict__
