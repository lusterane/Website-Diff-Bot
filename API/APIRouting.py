from flask import abort, make_response, request

from Services.APIUtils import APIUtils
from Services.FlaskAppInstance import app
from Services.LoggerContext import logger

'''
GET /api/jobs/{profile_id}
Description: get all jobs associated to a profile_id
Notes: will return empty jobs list if there are no jobs associated
'''


@app.route('/api/jobs', methods=['GET'])
def get_jobs_from_profile_id():
    try:
        profile_id = request.args.get('profile_id')

        jobs = APIUtils.get_jobs_from_profile_id(profile_id)
        return make_response({f'jobs': jobs}, 200)

    except Exception as e:
        logger.error(e)
        abort(400, description=e)


'''
GET api/diffs/{job_id}
Description: get all Diffs from a job
'''


@app.route('/api/diffs', methods=['GET'])
def get_diffs_from_job_id():
    try:
        job_id = request.args.get('job_id')

        diffs = APIUtils.get_diffs_from_job_id(job_id)
        return make_response({f'diffs': diffs}, 200)
    except Exception as e:
        logger.error(e)
        abort(400, description=e)


'''
GET api/checks/{job_id}
Description: get all Checks from a job
'''


@app.route('/api/checks', methods=['GET'])
def get_checks_from_job_id():
    try:
        job_id = request.args.get('job_id')

        checks = APIUtils.get_checks_from_job_id(job_id)
        return make_response({f'checks': checks}, 200)
    except Exception as e:
        logger.error(e)
        abort(400, description=e)


'''
GET /api/profiles/all
Description: get all profiles
'''


@app.route('/api/profiles/all', methods=['GET'])
def get_all_profiles():
    try:
        profiles = APIUtils.get_all_profiles()
        return make_response({f'profiles': profiles}, 200)
    except Exception as e:
        logger.error(e)
        abort(400, description=e)


'''
POST /api/jobs/create/{job_name}&{link}&{frequency}&{profile_id}
Description: Creates a job
Query Parameters:
* job_name: name of job
* link: https link associated to job
* frequency: frequency to refresh job (minutes)
    * 1hr = 60
    * 5hr = 300
    * 12hr = 720
    * 24hr = 1440
* profile_id: profile associated to job
'''


@app.route('/api/jobs/create', methods=['POST'])
def create_job():
    try:
        job_name = request.args.get('job_name')
        link = request.args.get('link')
        frequency = request.args.get('frequency')
        profile_id = request.args.get('profile_id')

        if not job_name or not link or not frequency or not profile_id:
            abort(400, description='Please provide all query parameters for this call\njob_name, link, frequency, profile_id')

        job = APIUtils.create_job(job_name, link, frequency, profile_id)
        return make_response({'job': job}, 200)

    except Exception as e:
        logger.error(e)
        abort(400, description=e)
'''
POST /api/jobs/all/refresh
Description: Refreshes all stale jobs
'''
@app.route('/api/jobs/all/refresh', methods=['POST'])
def refresh_jobs():
    try:
        jobs = APIUtils.refresh_stale_jobs()
        return make_response({'staleJobsUpdated': jobs}, 200)

    except Exception as e:
        logger.error(e)
        abort(400, description=e)

''' Helpers '''
if __name__ == '__main__':
    app.run(debug=True)
