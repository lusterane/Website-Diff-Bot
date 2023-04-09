import os
import random
from datetime import datetime, timezone
from enum import Enum

from supabase import create_client

from Models import *


class DatabaseManager:
    def __init__(self):
        self.supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        self.current_datetime = str(datetime.now(timezone.utc))
        self.user_table_name = os.environ.get(DBTable.User_Table_Name.value)
        self.html_table_name = os.environ.get(DBTable.HTML_Table_Name.value)
        self.html_user_relation_table_name = os.environ.get(DBTable.HTML_User_Relation_Table_Name.value)

    def update_tables_with_scrape_response(self, scraping_response: ScrapingResponseObject):
        # must create user before html entry because of foreign key relation
        html_object = self.__update_html_table(scraping_response)
        user_object = self.__update_user_table(scraping_response)
        relation_object = self.__update_relation_table(html_object, user_object)
        return True

    def __update_html_table(self, scraping_response: ScrapingResponseObject):
        html_response = self.__fetch_html_data_entry_with_link(scraping_response.link)
        if html_response.count:
            # if exists update html and datetime
            existing_entry = DBHTMLObject.from_json(html_response.data[0])

            existing_entry.html_data = scraping_response.html_data
            existing_entry.last_updated = self.current_datetime

            self.__update_html_data_entry_matching_link(existing_entry, scraping_response.link)

            return existing_entry
        else:
            # create new entry
            new_entry = DBHTMLObject(link=scraping_response.link,
                                     html_data=scraping_response.html_data, last_updated=self.current_datetime)
            self.__insert_html(new_entry)
            # TODO: throw error if primary key same as existing
            return new_entry

    def __update_user_table(self, scraping_response: ScrapingResponseObject) -> DBUserObject:
        user_response = self.__fetch_user_with_email(scraping_response.email)
        if user_response.count:
            # if exists, just return for relation table update
            return DBUserObject.from_json(user_response.data[0])
        else:
            # create new entry
            new_entry = DBUserObject(email=scraping_response.email)
            self.__insert_user(new_entry)
            # TODO: throw error if primary key same as existing
            return new_entry

    def __update_relation_table(self, html_object: DBHTMLObject, user_object: DBUserObject):
        relation_response = self.__fetch_relation_table(html_object, user_object)
        if relation_response.count:
            # if exists, just return
            return DBHTMLUserRelationObject.from_json(relation_response.data[0])
        else:
            # create new relation
            new_entry = DBHTMLUserRelationObject(id=self.__get_random_primary_key(), link=html_object.link,
                                                 email=user_object.email)
            self.__insert_relation(new_entry)
            # TODO: throw error if primary key same as existing
            return new_entry

    ''' Helper Methods '''

    # USER TABLE
    def __fetch_user_with_email(self, email):
        return self.supabase.table(self.user_table_name).select('*', count='exact').eq('email', email).execute()

    def __insert_user(self, entry):
        return self.supabase.table(self.user_table_name).insert(entry.__dict__, count='exact').execute()

    # HTML TABLE
    def __fetch_html_data_entry_with_link(self, link):
        return self.supabase.table(self.html_table_name).select('*', count='exact').eq('link', link).execute()

    def __insert_html(self, entry):
        return self.supabase.table(self.html_table_name).insert(entry.__dict__, count='exact').execute()

    def __update_html_data_entry_matching_link(self, entry, link):
        return self.supabase.table(self.html_table_name).update(entry.__dict__, count='exact').eq('link',
                                                                                                  link).execute()

    # RELATION TABLE
    def __fetch_relation_table(self, html_entry: DBHTMLObject, user_entry: DBUserObject):
        return self.supabase.table(self.html_user_relation_table_name).select('*', count='exact').eq('email',
                                                                                                     user_entry.email).eq(
            'link', html_entry.link).execute()

    def __insert_relation(self, entry):
        return self.supabase.table(self.html_user_relation_table_name).insert(entry.__dict__, count='exact').execute()

    def __get_random_primary_key(self):
        return random.randint(0, 99999)


class DBTable(Enum):
    HTML_Table_Name = "HTML_Table_Name"
    User_Table_Name = "Users_Table_Name"
    HTML_User_Relation_Table_Name = "HTML_User_Relation_Table_Name"
