from datetime import datetime

from Persistence.DBGateway import *
from Presentation.APIRouting import app
from Service.LoggerLauncher import LoggerLauncher


def main():
    LoggerLauncher.launch()
    app.run(debug=True)
    pass


def test_db():
    current_time = datetime.datetime.now()
    job_data = {
        'j_id': None,
        'job_name': 'UPDATED test job name',
        'link': 'https://google.com/',
        'frequency': '100',
        'last_updated': current_time,
        'next_update': current_time,
        'p_id': '1',
        's_id': '1',
        'up_id': '1'
    }
    print(Profile.create_profile('tobychow98@gmail.com'))
    print(ScrapedData.create_scraped_data('this is test scraped data'))
    print(Update.create_update('this is test update'))
    print(Job.create_job(job_data))
    print(Job.get_job_by_id(2))


if __name__ == '__main__':
    main()
