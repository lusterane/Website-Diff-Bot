from flask import abort, make_response, request

from Models.DBGateway import Profile
from Services.FlaskAppInstance import app
from Services.LoggerContext import logger
from Services.APIUtils import APIUtils

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
        abort(404, description=e)


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
        abort(404, description=e)


'''
GET /api/profiles/all
Description: get all profiles
'''


@app.route('/api/profiles/all')
def get_all_profiles():
    try:
        profiles = APIUtils.get_all_profiles()
        return make_response({f'profiles': profiles}, 200)
    except Exception as e:
        logger.error(e)
        abort(404, description=e)


''' Helpers '''
if __name__ == '__main__':
    app.run(debug=True)
