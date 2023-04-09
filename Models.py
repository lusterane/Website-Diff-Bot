'''
Users:
pk, email, name, link_pk

HTML_DATA_TABLE:
pk, link, html_data

'''


class ScrapingResponseObject:
    def __init__(self, link, html_data, email):
        self.link = link
        self.html_data = html_data
        self.email = email

    def __repr__(self):
        return f'Link: {self.link}\nEmail: {self.email}\nHtml Data:\n{self.html_data}\n'


class RequestObject:
    def __init__(self, email, link):
        self.email = email
        self.link = link


class DBHTMLObject:
    def __init__(self, link, html_data, last_updated='1990-01-01T00:00:00.965861+00:00'):
        self.link = link
        self.html_data = html_data
        self.last_updated = last_updated

    @staticmethod
    def from_json(json_dct):
        return DBHTMLObject(json_dct['link'],
                            json_dct['html_data'],
                            json_dct['last_updated'])


class DBUserObject:
    def __init__(self, email):
        self.email = email

    @staticmethod
    def from_json(json_dct):
        return DBUserObject(json_dct['email'])


class DBHTMLUserRelationObject:
    def __init__(self, id, link, email):
        self.id = id
        self.email = email
        self.link = link

    @staticmethod
    def from_json(json_dct):
        return DBHTMLUserRelationObject(json_dct['id'],
                                        json_dct['email'],
                                        json_dct['link'])
