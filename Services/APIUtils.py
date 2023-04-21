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
        diffs = job.scraped_data_entity.diffs
        return APIUtils.__jsonify_instrument_list__(diffs)

    @staticmethod
    def get_checks_from_job_id(job_id) -> []:
        job = Job.get_job_by_id(job_id)
        if not job:
            raise Exception(f'Job ID {job_id} does not exist')
        checks = job.scraped_data_entity.checks
        return APIUtils.__jsonify_instrument_list__(checks)

    '''
    returns job that's created
    '''

    @staticmethod
    def create_job(job_name, link, frequency, profile_id) -> {}:
        APIUtils.__validate_job_before_create_job__(job_name, link, profile_id)  # raises exception if not validated

        new_scraped_data = APIUtils.__get_scraped_data_for_link__(link)
        current_time = APIUtils.__get_current_time__()

        # insert Scraped Data Table
        s_id = ScrapedData.create_scraped_data(scraped_data=new_scraped_data, link=link).s_id

        # insert Checks Table
        Check.create_check(status=Check.Status.FirstCheck, s_id=s_id, checked_on=current_time)

        # insert Jobs Table
        job_data = {
            'job_name': job_name,
            'frequency': frequency,
            'last_updated': current_time,
            'next_update': APIUtils.__get_next_update_time__(last_updated=current_time, frequency=int(frequency)),
            'date_created': current_time,
            'p_id': profile_id,
            's_id': s_id
        }
        job = Job.create_job(job_data=job_data)

        return job.__json__()

    @staticmethod
    def refresh_stale_jobs() -> []:  # returns all jobs refreshed
        stale_jobs: [Job] = Job.get_stale_jobs()
        updated_stale_jobs: [Job] = []
        for stale_job in stale_jobs:
            # provide data
            stale_job_entity: Job = stale_job
            profile_entity: Profile = stale_job_entity.profile_entity
            scraped_data_entity: ScrapedData = stale_job_entity.scraped_data_entity

            new_scraped_data = APIUtils.__get_scraped_data_for_link__(scraped_data_entity.link)

            # refresh Jobs table
            APIUtils.__refresh_job__(stale_job_entity=stale_job_entity)

            # refresh Diffs table. returns check status
            check_status = APIUtils.__refresh_diffs_and_send_email__(scraped_data_entity=scraped_data_entity, profile_entity=profile_entity,
                                                                     new_scraped_data=new_scraped_data)

            # refresh Checks table
            Check.create_check(status=check_status, s_id=scraped_data_entity.s_id, checked_on=APIUtils.__get_current_time__())

            # refresh ScrapedData table
            APIUtils.__refresh_scraped_data__(scraped_data_entity=scraped_data_entity, new_scraped_data=new_scraped_data)

            updated_stale_jobs.append(stale_job_entity)

        return APIUtils.__jsonify_instrument_list__(updated_stale_jobs)

    ''' Helper Methods '''

    # ================ REFRESH_STALE_JOBS() ================
    @staticmethod
    def __refresh_job__(stale_job_entity: Job):
        current_time = APIUtils.__get_current_time__()
        job_data = {
            'job_name': stale_job_entity.job_name,
            'frequency': stale_job_entity.frequency,
            'last_updated': current_time,
            'next_update': APIUtils.__get_next_update_time__(last_updated=current_time, frequency=int(stale_job_entity.frequency))
        }
        updated_job = Job.update_job(j_id=stale_job_entity.j_id, job_data=job_data)
        return updated_job

    @staticmethod
    def __refresh_diffs_and_send_email__(scraped_data_entity: ScrapedData, profile_entity: Profile, new_scraped_data: str) -> Check.Status:
        s_id, old_scraped_data, link = scraped_data_entity.s_id, scraped_data_entity.scraped_data, scraped_data_entity.link

        diff_string = APIUtils.__get_html_diff__(old_scraped_data, new_scraped_data)  # returns empty string if no diff
        if diff_string:
            # send email if there's a diff
            Diff.create_diff(diff_string, s_id)
            try:
                from Services.EmailManager import EmailManager
                email_manager = EmailManager()
                email_manager.test_send_email_success(diff_string=diff_string, email=profile_entity.email, link=link)  # will raise exception if email not sent
                return Check.Status.AlertSent

            except Exception as e:
                # TODO: handle in email module
                logger.critical(f'Failed to send email Error: {e}')
                return Check.Status.AlertFailed
        else:
            return Check.Status.NoChange

    @staticmethod
    def __refresh_scraped_data__(scraped_data_entity: ScrapedData, new_scraped_data: str):
        new_scraped_data = ScrapedData.update_scraped_data(s_id=scraped_data_entity.s_id, new_scraped_data=new_scraped_data)
        return new_scraped_data

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

    # ================ CREATE_JOB() ================

    @staticmethod
    def __validate_job_before_create_job__(job_name, link, profile_id):
        profile = Profile.get_profile_by_id(profile_id)
        if not profile:
            raise Exception(f'Profile ID {profile_id} does not exist')

        # check if there's already a job with same job_name or link for a profile
        for job in profile.jobs:
            if job.job_name == job_name:
                raise Exception(f'Job with job name {job_name} already exists')
            elif job.scraped_data_entity.link == link:
                raise Exception(f'Job with link {link} already exists')

    # ================ GENERAL ================

    @staticmethod
    def __get_scraped_data_for_link__(link):
        from Services.WebsiteScraper import WebsiteScraper
        new_scraped_data = WebsiteScraper.scrape_link(link)
        return new_scraped_data

    @staticmethod
    def __get_next_update_time__(last_updated: datetime, frequency: int):
        return last_updated + datetime.timedelta(minutes=frequency)

    @staticmethod
    def __get_current_time__():
        return datetime.datetime.now()

    @staticmethod
    def __jsonify_instrument_list__(lis):
        return [k.__json__() for k in lis]
