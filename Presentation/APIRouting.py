from flask import abort, make_response, Flask
from Service.LoggerContext import logger

app = Flask(__name__)


@app.route('/hi', methods=['GET'])
def test():
    try:
        logger.info('from test')
        return make_response({'response': 'hi'}, 200)
    except Exception as e:
        abort(404, description=e)


''' Helpers '''
if __name__ == '__main__':
    app.run(debug=True)
