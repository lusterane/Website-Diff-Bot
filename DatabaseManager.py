import json
import os
import random
from datetime import datetime, timezone
from enum import Enum

from supabase import create_client

import Models


class DatabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)
        self.datetime = str(datetime.now(timezone.utc))

    def insert_data_test(self):
        data, count = self.supabase \
            .table('countries') \
            .insert({"id": 1, "name": "Denmark"}) \
            .execute()
        print(data, count)

    def update_tables_with_scrape_response(self, html_entry_object: Models.ScrapingResponseObject):
        html_response = self.__update_html_table(html_entry_object)
        user_response = self.__update_user_table(html_entry_object)

    def __update_html_table(self, entry_object: Models.ScrapingResponseObject):
        html_table_name = os.environ.get(DBTable.HTML_Table_Name.value)

        new_entry = Models.DBHTMLObject(random.randint(0, 99999), link=entry_object.link,
                                        html_data=entry_object.html_data, last_updated=self.datetime)

        # find if exists in db
        fetch_query_response = self.supabase.table(html_table_name).select('*', count='exact').eq('link',
                                                                                                  new_entry.link).execute()
        if fetch_query_response.count:
            # update existing
            response_data = fetch_query_response.data[0]
            new_entry.html_data_id = response_data['html_data_id']
            return self.supabase.table(html_table_name).update(new_entry.__dict__, count='exact').eq('link',
                                                                                                     new_entry.link).execute()
        return self.supabase.table(html_table_name).insert(new_entry.__dict__, count='exact').execute()

    def __update_user_table(self, entry_object: Models.ScrapingResponseObject):
        user_table_name = os.environ.get(DBTable.User_Table_Name.value)


class DBTable(Enum):
    HTML_Table_Name = "HTML_Table_Name"
    User_Table_Name = "Users_Table_Name"
