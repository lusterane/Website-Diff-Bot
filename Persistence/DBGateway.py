import os
from enum import Enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPABASE_CONNECTION_STRING")
db = SQLAlchemy(app)

# create tables if not existing
with app.app_context():
    db.create_all()


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
    def get_by_id(job_id):
        with app.app_context():
            return Job.query.filter_by(j_id=job_id).first()

    @staticmethod
    def get_all():
        with app.app_context():
            return Job.query.all()

    @staticmethod
    def create_job(job_data):
        with app.app_context():
            job = Job(
                j_id=job_data['j_id'],
                job_name=job_data['job_name'],
                link=job_data['link'],
                frequency=job_data['frequency'],
                last_updated=job_data['last_updated'],
                next_update=job_data['next_update'],
                p_id=job_data['p_id'],
                s_id=job_data['s_id'],
                up_id=job_data['up_id']
            )
            db.session.add(job)
            db.session.commit()
            refresh_session_if_needed(job)
            return job

    @staticmethod
    def update_job(job_id, job_data):
        with app.app_context():
            job = Job.query.filter_by(j_id=job_id).first()
            if job:
                job.job_name = job_data['job_name']
                job.link = job_data['link']
                job.frequency = job_data['frequency']
                job.next_update = job_data['next_update']
                job.p_id = job_data['p_id']
                job.s_id = job_data['s_id']
                job.up_id = job_data['up_id']
                job.last_updated = job_data['last_updated']
                db.session.commit()
                refresh_session_if_needed(job)
            return job

    def __repr__(self):
        return f"Job(j_id={self.j_id}, job_name='{self.job_name}', link='{self.link}', frequency={self.frequency}, last_updated='{self.last_updated}', " \
               f"next_update='{self.next_update}', p_id={self.p_id}, s_id={self.s_id}, up_id={self.up_id})"


class Profile(db.Model):
    __tablename__ = TableNames.PROFILES_TABLE.value

    p_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    jobs = db.relationship('Job', backref='profile', lazy=True)

    def __repr__(self):
        return f"Profile(p_id={self.p_id}, email='{self.email}')"


class ScrapedData(db.Model):
    __tablename__ = TableNames.SCRAPED_DATA_TABLE.value

    s_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    scraped_data = db.Column(db.Text, nullable=False)
    jobs = db.relationship('Job', backref='scrapeddata', lazy=True)

    def __repr__(self):
        return f"ScrapedData(s_id={self.s_id}, scraped_data='{get_truncated_html_data(self.scraped_data)}')"


class Update(db.Model):
    __tablename__ = TableNames.UPDATE_TABLE.value

    up_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    scraped_diff = db.Column(db.Text, nullable=False)
    updated_on = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    jobs = db.relationship('Job', backref='update', lazy=True)

    def __repr__(self):
        return f"Update(up_id={self.up_id}, scraped_diff='{self.scraped_diff}', updated_on='{self.updated_on}')"


''' Helpers '''


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
