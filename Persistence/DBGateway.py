import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

from Service.FlaskAppInstance import app

db = SQLAlchemy(app)
app.app_context().push()


class TableNames(Enum):
    JOBS_TABLE = 'JobsTable'
    PROFILES_TABLE = 'ProfilesTable'
    SCRAPED_DATA_TABLE = 'ScrapedDataTable'
    UPDATE_TABLE = 'UpdateTable'


class Job(db.Model):
    __tablename__ = TableNames.JOBS_TABLE.value

    j_id = db.Column(db.BigInteger, primary_key=True)
    job_name = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    next_update = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    p_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.PROFILES_TABLE.value}.p_id'))
    s_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.SCRAPED_DATA_TABLE.value}.s_id'))
    up_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.UPDATE_TABLE.value}.up_id'))

    @staticmethod
    def get_jobs():
        jobs = Job.query.all()
        return jobs

    @staticmethod
    def get_job_by_id(j_id):
        job = Job.query.get(j_id)
        return job

    @staticmethod
    def create_job(job_data):
        job = Job(job_name=job_data['job_name'], link=job_data['link'], frequency=job_data['frequency'],
                  last_updated=job_data['last_updated'], next_update=job_data['next_update'], p_id=job_data['p_id'],
                  s_id=job_data['s_id'], up_id=job_data['up_id'])
        db.session.add(job)
        db.session.commit()
        refresh_session_if_needed(job)
        return job

    @staticmethod
    def update_job(j_id, job_data):
        job = Job.query.get(j_id)
        if job:
            job.job_name = job_data['job_name']
            job.link = job_data['link']
            job.frequency = job_data['frequency']
            job.last_updated = job_data['last_updated']
            job.next_update = job_data['next_update']
            job.p_id = job_data['p_id']
            job.s_id = job_data['s_id']
            job.up_id = job_data['up_id']
            db.session.commit()
            refresh_session_if_needed(job)
        return job

    @staticmethod
    def delete_job(j_id):
        job = Job.query.get(j_id)
        if job:
            db.session.delete(job)
            db.session.commit()
            refresh_session_if_needed(job)
        return job

    def __json__(self):
        return {
            'j_id': self.j_id,
            'job_name': self.job_name,
            'link': self.link,
            'frequency': self.frequency,
            'last_updated': self.last_updated.isoformat(),
            'next_update': self.next_update.isoformat(),
            'p_id': self.p_id,
            's_id': self.s_id,
            'up_id': self.up_id,
        }

    def __repr__(self):
        return f"Job(j_id={self.j_id}, job_name='{self.job_name}', link='{self.link}', frequency={self.frequency}, last_updated='{self.last_updated}', " \
               f"next_update='{self.next_update}', p_id={self.p_id}, s_id={self.s_id}, up_id={self.up_id})"


class Profile(db.Model):
    __tablename__ = TableNames.PROFILES_TABLE.value

    p_id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    jobs = db.relationship('Job', backref='profile', lazy=True)

    @staticmethod
    def get_all_profiles():
        profiles = Profile.query.all()
        return profiles

    @staticmethod
    def get_profile_by_id(p_id):
        profile = Profile.query.get(p_id)
        return profile

    @staticmethod
    def create_profile(email):
        profile = Profile(email=email)
        db.session.add(profile)
        db.session.commit()
        refresh_session_if_needed(profile)
        return profile

    @staticmethod
    def update_profile(p_id, email):
        profile = Profile.query.get(p_id)
        if profile:
            profile.email = email
            db.session.commit()
            refresh_session_if_needed(profile)
        return profile

    @staticmethod
    def delete_profile(p_id):
        profile = Profile.query.get(p_id)
        if profile:
            db.session.delete(profile)
            db.session.commit()
            refresh_session_if_needed(profile)
        return profile

    def __json__(self):
        return {
            'p_id': self.p_id,
            'email': self.email,
        }

    def __repr__(self):
        return f"Profile(p_id={self.p_id}, email='{self.email}')"


class ScrapedData(db.Model):
    __tablename__ = TableNames.SCRAPED_DATA_TABLE.value

    s_id = db.Column(db.BigInteger, primary_key=True)
    scraped_data = db.Column(db.Text, nullable=False)
    jobs = db.relationship('Job', backref='scrapeddata', lazy=True)

    @staticmethod
    def get_scraped_data():
        scraped_data = ScrapedData.query.all()
        return scraped_data

    @staticmethod
    def get_scraped_data_by_id(s_id):
        scraped_data = ScrapedData.query.filter_by(s_id=s_id).first()
        return scraped_data

    @staticmethod
    def create_scraped_data(scraped_data):
        new_scraped_data = ScrapedData(scraped_data=scraped_data)
        db.session.add(new_scraped_data)
        db.session.commit()
        refresh_session_if_needed(new_scraped_data)
        return new_scraped_data

    @staticmethod
    def update_scraped_data(s_id, new_scraped_data):
        scraped_data = ScrapedData.query.filter_by(s_id=s_id).first()
        if scraped_data:
            scraped_data.scraped_data = new_scraped_data
            db.session.commit()
            refresh_session_if_needed(scraped_data)
        return scraped_data

    @staticmethod
    def delete_scraped_data(s_id):
        scraped_data = ScrapedData.query.filter_by(s_id=s_id).first()
        if scraped_data:
            db.session.delete(scraped_data)
            db.session.commit()
            refresh_session_if_needed(scraped_data)
        return scraped_data

    def __json__(self):
        return {
            's_id': self.s_id,
            'scraped_data': self.scraped_data,
        }

    def __repr__(self):
        return f"ScrapedData(s_id={self.s_id}, scraped_data='{get_truncated_html_data(self.scraped_data)}')"


class Update(db.Model):
    __tablename__ = TableNames.UPDATE_TABLE.value

    up_id = db.Column(db.BigInteger, primary_key=True)
    scraped_diff = db.Column(db.Text, nullable=False)
    updated_on = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    jobs = db.relationship('Job', backref='update', lazy=True)

    @staticmethod
    def get_all_updates():
        updates = Update.query.all()
        refresh_session_if_needed(updates)
        return updates

    @staticmethod
    def get_update_by_id(up_id):
        update = Update.query.filter_by(up_id=up_id).first()
        return update

    @staticmethod
    def create_update(scraped_diff):
        new_update = Update(scraped_diff=scraped_diff)
        new_update.updated_on = datetime.datetime.now()
        db.session.add(new_update)
        db.session.commit()
        refresh_session_if_needed(new_update)
        return new_update

    @staticmethod
    def update_updates(up_id, scraped_diff, updated_on):
        update = Update.query.get(up_id)
        if update:
            update.scraped_diff = scraped_diff
            update.updated_on = updated_on
            db.session.commit()
            refresh_session_if_needed(update)
        return update

    @staticmethod
    def delete_update(up_id):
        update = Update.query.get(up_id)
        if update:
            db.session.delete(update)
            db.session.commit()
            refresh_session_if_needed(update)
        return update

    def __json__(self):
        return {
            'up_id': self.up_id,
            'scraped_diff': self.scraped_diff,
            'updated_on': self.updated_on.isofortmat()
        }

    def __repr__(self):
        return f"Update(up_id={self.up_id}, scraped_diff='{self.scraped_diff}', updated_on='{self.updated_on}')"


''' Helpers '''
# create tables if not existing
db.create_all()


def refresh_session_if_needed(o: db.Model):
    if db.session.is_active:
        # call the refresh method to update the object with the latest values from the database
        db.session.refresh(o)
    else:
        # if the object is not attached to a session, attach it and then call the refresh method
        db.session.add(o)
        db.session.refresh(o)


def get_truncated_html_data(html_data):
    n = len(html_data)
    max_len_text = 200
    if n >= max_len_text:
        return html_data[:max_len_text] + ' ...'
    return html_data
