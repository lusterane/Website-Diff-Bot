class ScrapingResponseObject:
    def __init__(self, link, html_data, email):
        self.link = link
        self.html_data = html_data
        self.email = email

    def __repr__(self):
        return f'\nLink: {self.link}\nEmail: {self.email}\nHtml Data: {get_truncated_html_data(self.html_data)}\n'


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

    def __repr__(self):
        return f'\nLink: {self.link}\nHTML Data: {get_truncated_html_data(self.html_data)}\nLast Updated: {self.last_updated}\n'


class DBUserObject:
    def __init__(self, email):
        self.email = email

    @staticmethod
    def from_json(json_dct):
        return DBUserObject(json_dct['email'])

    def __repr__(self):
        return f'\nEmail: {self.email}'


class DBHTMLUserRelationObject:
    def __init__(self, id, email, link):
        self.id = id
        self.email = email
        self.link = link

    @staticmethod
    def from_json(json_dct):
        return DBHTMLUserRelationObject(json_dct['id'],
                                        json_dct['email'],
                                        json_dct['link'])

    def __repr__(self):
        return f'\nID: {self.id}\nEmail: {self.email}\nLink: {self.link}\n'


class DBUpdatedHTMLObject:
    def __init__(self, id, html_diff, updated_on, link):
        self.id = id
        self.html_diff = html_diff
        self.updated_on = updated_on
        self.link = link

    @staticmethod
    def from_json(json_dct):
        return DBUpdatedHTMLObject(json_dct['id'],
                                   json_dct['html_diff'],
                                   json_dct['updated_on'],
                                   json_dct['link'])

    def __repr__(self):
        return f'\nID: {self.id}\nHTML Diff: {get_truncated_html_data(self.html_diff)}\nUpdated On: {self.updated_on}\nLink: {self.link}\n'


def get_truncated_html_data(html_data):
    n = len(html_data)
    max_len_text = 200
    if n >= max_len_text:
        return html_data[:max_len_text] + '...'
    return html_data
