from datetime import datetime
from Presentation.APIRouting import app as api_flask_app
from Persistence.DBGateway import Profile, ScrapedData, Update, Job
import datetime
from Service.WebsiteScraper import WebsiteScraper
from Service.LoggerContext import logger


def main():
    # api_flask_app.run(debug=True)
    # logger.info('from main')
    WebsiteScraper.scrape_link('https://www.op.gg/')
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
