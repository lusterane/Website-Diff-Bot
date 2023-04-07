import json
from json import JSONEncoder
class HTMLEntryObjectModel:
    def __init__(self, customer, html_data, email):
        self.customer = customer
        self.html_data = html_data
        self.email = email
    def __repr__(self):
        return f'Customer: {self.customer}\nHtml Data:\n{self.html_data}\nEmail: {self.email}\n'

class RequestObject:
    def __init__(self, user, email, link):
        self.user = user
        self.email = email
        self.link = link


class HTMLEntryObjectEncoder(JSONEncoder):
    def default(self, o: HTMLEntryObjectModel) -> HTMLEntryObjectModel:
        return o.__dict__