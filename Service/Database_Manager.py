import logging
import random
from collections import defaultdict
from datetime import datetime, timezone

from postgrest.exceptions import APIError

from Persistence.Models import *
from Service.Database_Gateway import Database_Gateway
from Service.Website_Scraper import Website_Scraper


class DatabaseManager:
    def __init__(self):
        self.current_datetime = str(datetime.now(timezone.utc))
        self.db_gate = Database_Gateway()
        self.website_scraper = Website_Scraper()

    # expensive method !!!
    def update_tables_chron_job(self) -> dict:
        all_relations = self.__convert_relations_to_dict(self.db_gate.fetch_all_relations())  # dict {email:[link]}
        for email, link_lis in all_relations.items():
            for link in link_lis:
                # get scraping response
                scraping_request_object = RequestObject(email, link)
                scraping_response_object = self.website_scraper.scrape_request(scraping_request_object)

                # should always exist
                existing_html_db_entry = DBHTMLObject.from_json(
                    self.db_gate.fetch_html_data_entry_with_link(link).data[0])  # index 0 because there will always be one result

                old_html, new_html = existing_html_db_entry.html_data, scraping_response_object.html_data

                # update in html table
                self.__update_entry_in_html_table(existing_html_db_entry, new_html)

                # check diffs
                if old_html != new_html:
                    logging.info(f'Found Diff in {link} !!!')
                    html_diff = self.__get_html_diff(old_html, new_html)

                    existing_html_diff_entry = self.db_gate.fetch_html_diff_entry_with_link(link)

                    if existing_html_diff_entry.count:  # exists
                        self.__update_entry_in_updated_html_table(
                            DBUpdatedHTMLObject.from_json(existing_html_diff_entry.data[0]),
                            html_diff)
                    else:  # doesn't exist
                        self.__insert_entry_in_updated_html_table(html_diff, link)

        return all_relations

    # return false if both html and email exists
    def insert_email_link_into_tables(self, email, link) -> bool:
        html_response = self.db_gate.fetch_html_data_entry_with_link(link)
        email_response = self.db_gate.fetch_user_with_email(email)

        if html_response.count and email_response.count:
            return False
        if not html_response.count:
            # if html entry doesn't exist, do scraping and insert everything to table
            request_object = RequestObject(email, link)
            html_data = self.website_scraper.scrape_request(request_object).html_data

            self.db_gate.insert_into_html_table(DBHTMLObject(link, html_data, self.current_datetime))
        if not email_response.count:
            self.db_gate.insert_into_user_table(DBUserObject(email))

        # build relation since one of the entries doesn't exist
        self.db_gate.insert_relation(DBHTMLUserRelationObject(self.__get_random_primary_key(), link, email))
        return True

    ''' Helper Methods '''

    # update existing html table
    def __update_entry_in_html_table(self, existing_html_db_entry: DBHTMLObject, new_html_data) -> DBHTMLObject:
        # update data in entry
        existing_html_db_entry.html_data = new_html_data
        existing_html_db_entry.last_updated = self.current_datetime

        self.db_gate.update_html_data_entry_matching_link(existing_html_db_entry)

        return existing_html_db_entry

    def __update_entry_in_updated_html_table(self, existing_updated_html_db_entry: DBUpdatedHTMLObject,
                                             html_diff) -> DBUpdatedHTMLObject:
        existing_updated_html_db_entry.html_diff = html_diff
        existing_updated_html_db_entry.updated_on = self.current_datetime

        self.db_gate.update_html_diff_entry_matching_link(existing_updated_html_db_entry)

        return existing_updated_html_db_entry

    # TODO: maybe put these methods in model?
    def __insert_entry_in_updated_html_table(self, html_diff, link):
        for retry in range(3):  # 3 retries in-case of same primary key
            try:
                new_entry = DBUpdatedHTMLObject(id=self.__get_random_primary_key(),
                                                updated_on=self.current_datetime,
                                                html_diff=html_diff, link=link)
                self.db_gate.insert_html_diff(new_entry)
                return new_entry
            except APIError as e:
                logging.info(f'Got Error: {e}, Retrying {retry + 1}. . .')
        raise Exception

    # def fetch_all_users(self):
    #     response_objects = []
    #     response = self.supabase.table(self.user_table_name).select('*', count='exact').execute()
    #     if response.count:
    #         for data in response.data:
    #             response_objects.append(DBUserObject.from_json(data))
    #     return response_objects

    def __get_random_primary_key(self):
        return random.randint(0, 99999)

    def __get_html_diff(self, str1, str2) -> str:
        from difflib import SequenceMatcher

        matcher = SequenceMatcher(None, str1, str2)
        diff = matcher.get_opcodes()
        str_diffs = []
        for opcode, i1, i2, j1, j2 in diff:
            if opcode == 'delete':
                str_diffs.append('- %s' % str1[i1:i2])
            elif opcode == 'insert':
                str_diffs.append('+ %s' % str2[j1:j2])
            elif opcode == 'replace':
                str_diffs.append('- %s' % str1[i1:i2])
                str_diffs.append('+ %s' % str2[j1:j2])
        return '\n'.join(str_diffs)

    def __convert_relations_to_dict(self, all_relations_api_response):
        all_relations = defaultdict(list)
        if all_relations_api_response.count:
            for raw_data in all_relations_api_response.data:
                data = DBHTMLUserRelationObject.from_json(raw_data)
                all_relations[data.email].append(data.link)
        return all_relations
