import json
import os
from supabase import create_client, Client
import random
from Models import HTMLEntryObjectModel

class DatabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)

    def insert_data_test(self):
        data, count = self.supabase\
            .table('countries')\
            .insert({"id": 1, "name": "Denmark"})\
            .execute()
        print(data, count)

    def insert_html_data(self, htmlEntryObject: HTMLEntryObjectModel):
        insert_object = {
            'id': random.randint(0, 99999),
            'customer': htmlEntryObject.customer,
            'html_data': htmlEntryObject.html_data,
            'email': htmlEntryObject.email
        }
        data, count = self.supabase.table('Scraped_HTML_Data').insert(insert_object).execute()
        print(data, count)
    def serialize_json(self, dict):
        json_object = json.dumps(dict, indent=4)
