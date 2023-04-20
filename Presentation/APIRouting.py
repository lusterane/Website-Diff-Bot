from flask import abort, make_response, request, Flask, jsonify

from Persistence.DBGateway import Profile, Job
from Service.LoggerContext import logger
from Service.FlaskAppInstance import app

'''
GET /api/users/{profile_id}
Description: get all jobs associated to a profile_id
Notes: will return empty jobs list if there are no jobs associated

200 -> profile found
201 -> profile not found

'''


@app.route('/api/jobs', methods=['GET'])
def get_jobs_from_profile_id():
    try:
        profile_id = request.args.get('profile_id')
        profile = Profile.get_profile_by_id(profile_id)
        if profile:
            jobs = [job.__json__() for job in profile.jobs]
            return make_response({f'jobs': jobs}, 200)
        return make_response({'message': f'Profile id {profile_id} not found.'}, 201)
    except Exception as e:
        logger.error(e)
        abort(404, description=e)


''' Helpers '''
if __name__ == '__main__':
    app.run(debug=True)
