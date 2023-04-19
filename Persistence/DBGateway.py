from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy as sa
from enum import Enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPABASE_CONNECTION_STRING")
db = SQLAlchemy(app)


class TableNames(Enum):
    JOBS_TABLE = 'JobsTable'
    PROFILES_TABLE = 'ProfilesTable'
    SCRAPED_DATA_TABLE = 'ScrapedDataTable'
    UPDATE_TABLE = 'UpdateTable'


class Job(db.Model):
    __tablename__ = TableNames.JOBS_TABLE.value

    j_id = db.Column(db.BigInteger, primary_key=True)
    job_name = db.Column(db.Text)
    link = db.Column(db.Text)
    frequency = db.Column(db.Integer)
    last_updated = db.Column(db.TIMESTAMP(timezone=True))
    next_update = db.Column(db.TIMESTAMP(timezone=True))
    p_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.PROFILES_TABLE.value}.p_id'))
    s_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.SCRAPED_DATA_TABLE.value}.s_id'))
    up_id = db.Column(db.BigInteger, db.ForeignKey(f'{TableNames.UPDATE_TABLE.value}.up_id'))

    def __repr__(self):
        return f"Job(j_id={self.j_id}, job_name='{self.job_name}', link='{self.link}', frequency={self.frequency}, last_updated='{self.last_updated}', " \
               f"next_update='{self.next_update}', p_id={self.p_id}, s_id={self.s_id}, up_id={self.up_id})"


class Profile(db.Model):
    __tablename__ = TableNames.PROFILES_TABLE.value

    p_id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text)
    jobs = db.relationship('Job', backref='profile', lazy=True)

    def __repr__(self):
        return f"Profile(p_id={self.p_id}, email='{self.email}')"


class ScrapedData(db.Model):
    __tablename__ = TableNames.SCRAPED_DATA_TABLE.value

    s_id = db.Column(db.BigInteger, primary_key=True)
    scraped_data = db.Column(db.Text)
    jobs = db.relationship('Job', backref='scrapeddata', lazy=True)

    def __repr__(self):
        return f"ScrapedData(s_id={self.s_id}, scraped_data='{self.scraped_data}')"


class Update(db.Model):
    __tablename__ = TableNames.UPDATE_TABLE.value

    up_id = db.Column(db.BigInteger, primary_key=True)
    scraped_diff = db.Column(db.Text)
    updated_on = db.Column(db.TIMESTAMP(timezone=True))
    jobs = db.relationship('Job', backref='update', lazy=True)

    def __repr__(self):
        return f"Update(up_id={self.up_id}, scraped_diff='{self.scraped_diff}', updated_on='{self.updated_on}')"


with app.app_context():
    db.create_all()
    jobs = Job.query.all()
    profiles = Profile.query.all()
    for profile in profiles:
        print(profile)


def get_truncated_html_data(html_data):
    n = len(html_data)
    max_len_text = 200
    if n >= max_len_text:
        return html_data[:max_len_text] + ' ...'
    return html_data
