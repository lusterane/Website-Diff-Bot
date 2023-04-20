from flask import abort, make_response, request

from Models.DBGateway import Profile
from Services.FlaskAppInstance import app
from Services.LoggerContext import logger

'''
GET /api/jobs/{profile_id}
Description: get all jobs associated to a profile_id
Notes: will return empty jobs list if there are no jobs associated

200 -> profile found
300 -> profile not found

'''


@app.route('/api/jobs', methods=['GET'])
def get_jobs_from_profile_id():
    try:
        profile_id = request.args.get('profile_id')
        profile = Profile.get_profile_by_id(profile_id)
        if profile:
            jobs = [job.__json__() for job in profile.jobs]
            return make_response({f'jobs': jobs}, 200)
        return make_response({'message': f'Profile id {profile_id} not found.'}, 300)
    except Exception as e:
        logger.error(e)
        abort(404, description=e)


'''
GET /updates/{job_id}
Description: get all Updates from a job

200 -> job found
300 -> job not found
FKKKK 
M:M Job and Update table??
'''


@app.route('/api/updates', methods=['GET'])
def get_updates_from_job_id():
    try:
        # job_id = request.args.get('job_id')
        # job = Job.get_job_by_id(job_id)
        # if job:
        #     updates = [job.__json__() for job in profile.jobs]
        #     return make_response({f'jobs': jobs}, 200)
        return make_response({'message': f'Job id {job_id} not found.'}, 300)
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
        profiles = [profile.__json__() for profile in Profile.get_all_profiles()]
        return make_response({f'profiles': profiles}, 200)
    except Exception as e:
        logger.error(e)
        abort(404, description=e)


''' Helpers '''
if __name__ == '__main__':
    app.run(debug=True)
