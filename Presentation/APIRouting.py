import logging

from flask import request, abort, make_response

from Service.FlaskInitializationService import FlaskInitializationService

# initialization
init_object = FlaskInitializationService()
app = init_object.app
website_scraper = init_object.website_scraper
dm = init_object.dm


# if email or link doesn't exist, it will insert
# if already exists, return 202
@app.route('/all/insertEmailAndLink', methods=['POST'])
def insertEmailAndLink():
    __api_log(f'Call {insertEmailAndLink.__name__}')
    try:
        email = request.args.get('email', type=str)
        link = request.args.get('link', type=str)
        response = dm.insert_email_link_into_tables(email, link)
        if response:
            return make_response({'body': f'Inserted {link} for {email} into table'}, 200)
        return make_response({'body': f'Did not insert {link} for {email}'}, 202)
    except Exception as e:
        __api_log(e)
        abort(404, description=e)


def __api_log(e):
    logging.info(f'API: {e}')


if __name__ == '__main__':
    app.run(debug=True)
