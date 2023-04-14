import logging
import os
from enum import Enum

from supabase import create_client

from Persistence.Models import *


class Database_Gateway:
    def __init__(self):
        self.supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        self.user_table_name = os.environ.get(DBTable.User_Table_Name.value)
        self.html_table_name = os.environ.get(DBTable.HTML_Table_Name.value)
        self.updated_html_table_name = os.environ.get(DBTable.HTML_Diff_Table_Name.value)
        self.html_user_relation_table_name = os.environ.get(DBTable.HTML_User_Relation_Table_Name.value)

    # USER TABLE
    def fetch_user_with_email(self, email):
        logging.info(f"DB calling {self.fetch_user_with_email.__name__} with {email}")
        return self.supabase.table(self.user_table_name).select('*', count='exact').eq('email', email).execute()

    def insert_into_user_table(self, entry):
        logging.info(f"DB calling {self.insert_into_user_table.__name__} with {entry}")
        return self.supabase.table(self.user_table_name).insert(entry.__dict__, count='exact').execute()

    # HTML TABLE
    def fetch_html_data_entry_with_link(self, link):
        logging.info(f"DB calling {self.fetch_html_data_entry_with_link.__name__} with {link}")
        return self.supabase.table(self.html_table_name).select('*', count='exact').eq('link', link).execute()

    def insert_into_html_table(self, entry):
        logging.info(f"DB calling {self.insert_into_html_table.__name__} with {entry}")
        return self.supabase.table(self.html_table_name).insert(entry.__dict__, count='exact').execute()

    def update_html_data_entry_matching_link(self, entry):
        logging.info(f"DB calling {self.update_html_data_entry_matching_link.__name__} with {entry}")
        return self.supabase.table(self.html_table_name).update(entry.__dict__, count='exact').eq('link',
                                                                                                  entry.link).execute()

    # RELATION TABLE
    def fetch_relation_table(self, html_entry: DBHTMLObject, user_entry: DBUserObject):
        logging.info(f"DB calling {self.fetch_relation_table.__name__} with {html_entry} and {user_entry}")
        return self.supabase.table(self.html_user_relation_table_name).select('*', count='exact').eq('email',
                                                                                                     user_entry.email).eq(
            'link', html_entry.link).execute()

    def fetch_all_relations(self):
        logging.info(f"DB calling {self.fetch_all_relations.__name__}")
        return self.supabase.table(self.html_user_relation_table_name).select('*', count='exact').execute()

    def insert_relation(self, entry):
        logging.info(f"DB calling {self.insert_relation.__name__} with {entry}")
        return self.supabase.table(self.html_user_relation_table_name).insert(entry.__dict__,
                                                                              count='exact').execute()

    # UPDATED HTML TABLE
    def fetch_html_diff_entry_with_link(self, link):
        logging.info(f"DB calling {self.fetch_html_diff_entry_with_link.__name__} with {link}")
        return self.supabase.table(self.updated_html_table_name).select('*', count='exact').eq('link',
                                                                                               link).execute()

    def update_html_diff_entry_matching_link(self, entry):
        logging.info(f"DB calling {self.update_html_diff_entry_matching_link.__name__} with {entry}")
        return self.supabase.table(self.updated_html_table_name).update(entry.__dict__, count='exact').eq('link',
                                                                                                          entry.link).execute()

    def insert_html_diff(self, entry):
        logging.info(f"DB calling {self.insert_html_diff.__name__} with {entry}")
        return self.supabase.table(self.updated_html_table_name).insert(entry.__dict__, count='exact').execute()


class DBTable(Enum):
    HTML_Table_Name = "HTML_Table_Name"
    User_Table_Name = "Users_Table_Name"
    HTML_User_Relation_Table_Name = "HTML_User_Relation_Table_Name"
    HTML_Diff_Table_Name = "HTML_Diff_Table_Name"
