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

class DBHTMLObject:
    def __init__(self, html_data_id, link, html_data, last_updated='1990-01-01T00:00:00.965861+00:00'):
        self.html_data_id = html_data_id
        self.link = link
        self.html_data = html_data
        self.last_updated = last_updated

    @staticmethod
    def from_json(json_dct):
        return DBHTMLObject(json_dct['html_data_id'],
                            json_dct['link'],
                            json_dct['html_data'],
                            json_dct['last_updated'])


class DBUserObject:
    def __init__(self, user_data_id, email, name, html_data_fk):
        self.user_data_id = user_data_id
        self.email = email
        self.name = name
        self.html_data_fk = html_data_fk
