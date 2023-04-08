import json
import os
from supabase import create_client, Client
import random
import Models
from enum import Enum

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

    def update_tables_with_response_objects(self, html_entry_objects: [Models.ScrapingResponseObject]):
        for html_entry_object in html_entry_objects:
            self.__update_html_table(html_entry_object)
            self.__update_user_table(html_entry_object)

    def __update_html_table(self, entry_object: Models.ScrapingResponseObject):
        html_table_name = os.environ.get(DBTable.HTML_Table_Name.value)
        data, count = None, None
        def find_entry():

            return None
        exists = find_entry()
        if exists:
            # replace entry
            pass
        else:
            # add new entry
            new_entry = {
                'html_data_id': random.randint(0, 99999),
                'link': entry_object.link,
                'html_data': entry_object.html_data
            }
            data, count = self.supabase.table(html_table_name).insert(new_entry).execute()
        return data, count
    def __update_user_table(self, entry_object: Models.ScrapingResponseObject):
        user_table_name = os.environ.get(DBTable.User_Table_Name.value)
    def serialize_json(self, dict):
        json_object = json.dumps(dict, indent=4)

class DBTable(Enum):
    HTML_Table_Name = "HTML_Table_Name"
    User_Table_Name = "Users_Table_Name"