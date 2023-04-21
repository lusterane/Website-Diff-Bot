import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

from Services.FlaskAppInstance import app

db = SQLAlchemy(app)
app.app_context().push()


class TableNames(Enum):
    JOBS_TABLE = 'JobsTable'
    PROFILES_TABLE = 'ProfilesTable'
    SCRAPED_DATA_TABLE = 'ScrapedDataTable'
    DIFFS_TABLE = 'DiffsTable'
    CHECKS_TABLE = 'ChecksTable'


class Job(db.Model):
    __tablename__ = TableNames.JOBS_TABLE.value

    j_id = db.Column(db.BigInteger, primary_key=True)
    job_name = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    next_update = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    date_created = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    p_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.PROFILES_TABLE.value}.p_id'))
    s_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.SCRAPED_DATA_TABLE.value}.s_id'))

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
        job = Job(job_name=job_data['job_name'], frequency=job_data['frequency'],
                  last_updated=job_data['last_updated'], next_update=job_data['next_update'], date_created=datetime.datetime.now(), p_id=job_data['p_id'],
                  s_id=job_data['s_id'])
        db.session.add(job)
        db.session.commit()
        refresh_session_if_needed(job)
        return job

    '''
    only let user update job_name and frequency
    '''

    @staticmethod
    def update_job(j_id, job_data):
        job = Job.query.get(j_id)
        if job:
            job.job_name = job_data['job_name']
            job.frequency = job_data['frequency']
            job.last_updated = job_data['last_updated']
            job.next_update = job_data['next_update']
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
            'frequency': self.frequency,
            'last_updated': self.last_updated.isoformat(),
            'next_update': self.next_update.isoformat(),
            'date_created': self.date_created.isoformat(),
            'p_id': self.p_id,
            's_id': self.s_id,
        }

    def __repr__(self):
        return f"Job(j_id={self.j_id}, job_name='{self.job_name}', frequency={self.frequency}, last_updated='{self.last_updated}', " \
               f"next_update='{self.next_update}', data_created='{self.date_created}', p_id={self.p_id}, s_id={self.s_id})"


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
    link = db.Column(db.Text, nullable=False, unique=True)
    jobs = db.relationship('Job', backref='scraped_data', lazy=True)
    diffs = db.relationship('Diff', backref='scraped_data', lazy=True)
    checks = db.relationship('Check', backref='scraped_data', lazy=True)

    @staticmethod
    def get_all_scraped_data():
        scraped_data = ScrapedData.query.all()
        return scraped_data

    @staticmethod
    def get_scraped_data_by_id(s_id):
        scraped_data = ScrapedData.query.filter_by(s_id=s_id).first()
        return scraped_data

    @staticmethod
    def get_scraped_data_by_link(link):
        scraped_data = ScrapedData.query.filter_by(link=link).first()
        return scraped_data

    @staticmethod
    def create_scraped_data(scraped_data, link):
        new_scraped_data = ScrapedData(scraped_data=scraped_data, link=link)
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
            'link': self.link
        }

    def __repr__(self):
        return f"ScrapedData(s_id={self.s_id}, scraped_data='{get_truncated_html_data(self.scraped_data)},link='{self.link}')"


class Diff(db.Model):
    __tablename__ = TableNames.DIFFS_TABLE.value

    d_id = db.Column(db.BigInteger, primary_key=True)
    scraped_diff = db.Column(db.Text, nullable=False)
    updated_on = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    s_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.SCRAPED_DATA_TABLE.value}.s_id'))

    @staticmethod
    def get_all_diffs():
        diffs = Diff.query.all()
        refresh_session_if_needed(diffs)
        return diffs

    @staticmethod
    def get_diff_by_id(d_id):
        diff = Diff.query.filter_by(d_id=d_id).first()
        return diff

    @staticmethod
    def create_diff(scraped_diff, s_id):
        diff = Diff(scraped_diff=scraped_diff, s_id=s_id)
        diff.updated_on = datetime.datetime.now()
        db.session.add(diff)
        db.session.commit()
        refresh_session_if_needed(diff)
        return diff

    @staticmethod
    def update_diff(d_id, scraped_diff, updated_on, s_id):
        diff = Diff.query.get(d_id)
        if diff:
            diff.scraped_diff = scraped_diff
            diff.updated_on = updated_on
            diff.s_id = s_id
            db.session.commit()
            refresh_session_if_needed(diff)
        return diff

    @staticmethod
    def delete_diff(d_id):
        diff = Diff.query.get(d_id)
        if diff:
            db.session.delete(diff)
            db.session.commit()
            refresh_session_if_needed(diff)
        return diff

    def __json__(self):
        return {
            'd_id': self.d_id,
            'scraped_diff': self.scraped_diff,
            'updated_on': self.updated_on.isoformat(),
            's_id': self.s_id
        }

    def __repr__(self):
        return f"Diff(d_id={self.d_id}, scraped_diff='{self.scraped_diff}', updated_on='{self.updated_on}, s_id='{self.s_id}')"


class Check(db.Model):
    __tablename__ = TableNames.CHECKS_TABLE.value

    c_id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column(db.Text, nullable=False)
    checked_on = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    s_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.SCRAPED_DATA_TABLE.value}.s_id'))

    class Status(Enum):
        AlertSent = 'Sent Alert'
        FirstCheck = 'First Check'
        NoChange = 'No Change'
        SendAlertFailed = 'Failed To Send Alert'
        pass

    @staticmethod
    def get_all_checks():
        checks = Check.query.all()
        refresh_session_if_needed(checks)
        return checks

    @staticmethod
    def get_check_by_id(c_id):
        check = Check.query.filter_by(c_id=c_id).first()
        return check

    @staticmethod
    def create_check(status: Status, s_id):
        check = Check(status=status.value, s_id=s_id)
        check.checked_on = datetime.datetime.now()
        db.session.add(check)
        db.session.commit()
        refresh_session_if_needed(check)
        return check

    @staticmethod
    def update_check(c_id, status: Status, checked_on, s_id):
        check = Check.query.get(c_id)
        if check:
            check.status = status.value
            check.checked_on = checked_on
            check.s_id = s_id
            db.session.commit()
            refresh_session_if_needed(check)
        return check

    @staticmethod
    def delete_check(c_id):
        check = Check.query.get(c_id)
        if check:
            db.session.delete(check)
            db.session.commit()
            refresh_session_if_needed(check)
        return check

    def __json__(self):
        return {
            'c_id': self.c_id,
            'status': self.status,
            'checked_on': self.checked_on.isoformat(),
            's_id': self.s_id
        }

    def __repr__(self):
        return f"Check(c_id={self.c_id}, status='{self.status}', checked_on='{self.checked_on}, s_id='{self.s_id}')"


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
