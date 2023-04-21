import re

from Models.DBGateway import *
from Services.LoggerContext import logger


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

    '''
    returns job that's created
    '''

    @staticmethod
    def create_job(job_name, link, frequency, profile_id) -> {}:
        APIUtils.__validate_job_before_create_job__(job_name, link, profile_id)  # raises exception if not validated

        from Services.WebsiteScraper import WebsiteScraper
        new_scraped_data = WebsiteScraper.scrape_link(link)

        s_id = ScrapedData.create_scraped_data(scraped_data=new_scraped_data, link=link).s_id

        current_time = APIUtils.__get_current_time__()
        check = Check.create_check(status=Check.Status.FirstCheck, s_id=s_id, checked_on=current_time)
        job_data = {
            'job_name': job_name,
            'frequency': frequency,
            'last_updated': current_time,
            'next_update': APIUtils.__get_next_update_time__(last_updated=current_time, frequency=int(frequency)),
            'p_id': profile_id,
            's_id': s_id
        }
        return Job.create_job(job_data=job_data).__json__()

    ''' Helper Methods '''

    @staticmethod
    def __validate_job_before_create_job__(job_name, link, profile_id):
        profile = Profile.get_profile_by_id(profile_id)
        if not profile:
            raise Exception(f'Profile ID {profile_id} does not exist')

        # check if there's already a job with same job_name or link for a profile
        for job in profile.jobs:
            if job.job_name == job_name:
                raise Exception(f'Job with job name {job_name} already exists')
            elif job.scraped_data.link == link:
                raise Exception(f'Job with link {link} already exists')

    # pass job only if in update job flow !
    # updates/inserts ScrapedData, Check, Job. if necessary, inserts Diff.
    @staticmethod
    def __refresh_all_tables__(job_name, link, frequency, profile_id, job: Job = None) -> Job:  # return time job is refreshed
        # if job:
        #     # UPDATE_JOB FLOW
        #     old_scraped_data_entity = job.scraped_data.scraped_data  # will always exist
        #     ScrapedData.update_scraped_data(s_id=old_scraped_data_entity.s_id, new_scraped_data=new_scraped_data)
        # else:
        # # CREATE_JOB FLOW
        #
        # s_id, old_scraped_data = old_scraped_data_entity.s_id, old_scraped_data_entity.scraped_data
        #
        # diff_string = APIUtils.__get_html_diff__(old_scraped_data, new_scraped_data)  # returns empty string if no diff
        # if diff_string:
        #     Diff.create_diff(diff_string, s_id)
        #     try:
        #         from Services.EmailManager import EmailManager
        #         email_manager = EmailManager()
        #         email_manager.test_send_email_success()
        #         check = Check.create_check(status=Check.Status.AlertSent, s_id=s_id)
        #     except Exception as e:
        #         check = Check.create_check(status=Check.Status.SendAlertFailed, s_id=s_id)
        #         logger.critical('Failed to send email Error:', e)
        # else:
        #     check = Check.create_check(status=Check.Status.NoChange, s_id=s_id)
        # last_updated = check.checked_on
        # job_data = {
        #     'job_name': job_name,
        #     'frequency': frequency,
        #     'last_updated': last_updated,
        #     'next_update': APIUtils.__get_next_update_time__(last_updated=last_updated, frequency=int(frequency)),
        #     'p_id': profile_id,
        #     's_id': old_scraped_data_entity.s_id
        # }
        # return Job.create_job(job_data=job_data).__json__()
        return None

    @staticmethod
    def __get_next_update_time__(last_updated: datetime, frequency: int):
        return last_updated + datetime.timedelta(minutes=frequency)

    @staticmethod
    def __get_current_time__():
        return datetime.datetime.now()

    @staticmethod
    def __jsonify_instrument_list__(lis):
        return [k.__json__() for k in lis]

    @staticmethod
    def __get_html_diff__(str1, str2) -> str:
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
