import logging

from flask import abort, make_response, Flask

app = Flask(__name__)


# if email or link doesn't exist, it will insert
# if already exists, return 202
@app.route('/hi', methods=['GET'])
def test():
    # __api_log__(f'Call {test.__name__}')
    try:
        return make_response({'response': 'hi'}, 200)
    except Exception as e:
        # __api_log__(e)
        abort(404, description=e)


''' Helpers '''


def __api_log__(e):
    logging.info(f'API: {e}')


if __name__ == '__main__':
    app.run(debug=True)
