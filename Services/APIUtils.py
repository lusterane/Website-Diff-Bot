import re
from datetime import datetime, timezone

from Models.DBGateway import *


class APIUtils:

    @staticmethod
    def get_jobs_from_profile_id(profile_id) -> []:
        profile = Profile.get_profile_by_id(profile_id)
        if not profile:
            raise Exception(f'Profile ID {profile_id} does not exist')
        jobs = profile.jobs
        return APIUtils.__jsonify_instrument_list__(jobs)

    @staticmethod
    def get_all_profiles() -> []:
        profiles = Profile.get_all_profiles()
        APIUtils.__jsonify_instrument_list__(profiles)

    @staticmethod
    def get_diffs_from_job_id(job_id) -> []:
        job = Job.get_job_by_id(job_id)
        if not job:
            raise Exception(f'Job ID {job_id} does not exist')
        diffs = job.scraped_data.diffs
        return APIUtils.__jsonify_instrument_list__(diffs)

    @staticmethod
    def get_checks_from_job_id(job_id) -> []:
        job = Job.get_job_by_id(job_id)
        if not job:
            raise Exception(f'Job ID {job_id} does not exist')
        checks = job.scraped_data.checks
        return APIUtils.__jsonify_instrument_list__(checks)

    ''' Helper Methods '''

    @staticmethod
    def __jsonify_instrument_list__(lis):
        return [k.__json__() for k in lis]

    @staticmethod
    def __get_current_time__() -> str:
        return str(datetime.now(timezone.utc))

    @staticmethod
    def __get_html_diff(str1, str2) -> str:
        # if there's no diff, give empty string
        if str1 == str2:
            return ''

        from difflib import SequenceMatcher

        matcher = SequenceMatcher(None, str1, str2)
        diff = matcher.get_opcodes()
        str_diffs = []
        for opcode, i1, i2, j1, j2 in diff:
            if opcode == 'delete':
                processed_str = APIUtils.__preprocess_diff__(str1[i1:i2])
                if not processed_str:
                    continue
                str_diffs.append('- %s' % processed_str)
            elif opcode == 'insert':
                processed_str = APIUtils.__preprocess_diff__(str2[j1:j2])
                if not processed_str:
                    continue
                str_diffs.append('+ %s' % processed_str)
            elif opcode == 'replace':
                processed_str1 = APIUtils.__preprocess_diff__(str2[i1:i2])
                processed_str2 = APIUtils.__preprocess_diff__(str2[j1:j2])
                if not processed_str1 or not processed_str2:
                    continue
                str_diffs.append('- %s' % processed_str1)
                str_diffs.append('+ %s' % processed_str2)
        return '\n'.join(str_diffs)

    @staticmethod
    def __preprocess_diff__(diff):
        new_diff = diff.strip()

        # remove all spaces and see if it is a digit
        if re.sub(r'\s+', '', new_diff).isdigit():
            return ''

        for content in new_diff.split(','):
            # if any are not numbers, then content is valid
            if not content.isdigit():
                return new_diff
        return ''
