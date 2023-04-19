import inspect
import logging
import random
import re
from collections import defaultdict
from datetime import datetime, timezone

from postgrest.exceptions import APIError

from Persistence.DBGateway import *
from Service.Helper.ExceptionHelper import ExceptionHelper
from Service.WebsiteScraper import WebsiteScraper


class DatabaseManager:
    def __init__(self):
        self.current_datetime = str(datetime.now(timezone.utc))
        self.db_gate = DatabaseGateway()
        self.website_scraper = WebsiteScraper()

    ''' Helper Methods '''

    def __get_html_diff(self, str1, str2) -> str:
        # if there's no diff, give empty string
        if str1 == str2:
            return ''

        from difflib import SequenceMatcher

        matcher = SequenceMatcher(None, str1, str2)
        diff = matcher.get_opcodes()
        str_diffs = []
        for opcode, i1, i2, j1, j2 in diff:
            if opcode == 'delete':
                processed_str = self.__preprocess_diff(str1[i1:i2])
                if not processed_str:
                    continue
                str_diffs.append('- %s' % processed_str)
            elif opcode == 'insert':
                processed_str = self.__preprocess_diff(str2[j1:j2])
                if not processed_str:
                    continue
                str_diffs.append('+ %s' % processed_str)
            elif opcode == 'replace':
                processed_str1 = self.__preprocess_diff(str2[i1:i2])
                processed_str2 = self.__preprocess_diff(str2[j1:j2])
                if not processed_str1 or not processed_str2:
                    continue
                str_diffs.append('- %s' % processed_str1)
                str_diffs.append('+ %s' % processed_str2)
        return '\n'.join(str_diffs)

    def __preprocess_diff(self, diff):
        new_diff = diff.strip()

        # remove all spaces and see if it is a digit
        if re.sub(r'\s+', '', new_diff).isdigit():
            return ''

        for content in new_diff.split(','):
            # if any are not numbers, then content is valid
            if not content.isdigit():
                return new_diff
        return ''
