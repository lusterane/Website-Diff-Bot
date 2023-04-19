# import os
# import unittest
# from datetime import datetime
#
# from Persistence.DBGateway import app, db, Job, Profile, ScrapedData, Update
#
#
# class TestModels(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Set up the database before running the tests
#         app.config['TESTING'] = True
#         # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPABASE_CONNECTION_STRING")
#         with app.app_context():
#             db.create_all()
#
#     def setUp(self):
#         # Create test data for each test
#
#         self.profile = Profile.create_profile('test@test.com')
#         self.scraped_data = ScrapedData.create_scraped_data('test data')
#         self.update = Update.create_update('test scraped diff', datetime.utcnow())
#         self.job = Job.create_job({
#             'job_name': 'Test Job',
#             'link': 'http://example.com',
#             'frequency': 60,
#             'last_updated': datetime.utcnow(),
#             'next_update': datetime.utcnow(),
#             'p_id': self.profile.p_id,
#             's_id': self.scraped_data.s_id,
#             'up_id': self.update.up_id
#         })
#
#     def tearDown(self):
#         # Delete test data after each test
#         with app.app_context():
#             db.session.delete(self.job)
#             db.session.delete(self.scraped_data)
#             db.session.delete(self.profile)
#             db.session.delete(self.update)
#             db.session.commit()
#
#     @classmethod
#     def tearDownClass(cls):
#         # Clean up the database after running the tests
#         with app.app_context():
#             db.session.remove()
#             db.drop_all()
#
#     def test_get_jobs(self):
#         jobs = Job.get_jobs()
#         self.assertIsNotNone(jobs)
#
#     def test_get_job_by_id(self):
#         job = Job.get_job_by_id(self.job.j_id)
#         self.assertEqual(job.job_name, 'Test Job')
#
#     def test_create_job(self):
#         new_job = Job.create_job({
#             'job_name': 'New Job',
#             'link': 'http://example.com',
#             'frequency': 60,
#             'last_updated': datetime.utcnow(),
#             'next_update': datetime.utcnow(),
#             'p_id': self.profile.p_id,
#             's_id': self.scraped_data.s_id,
#             'up_id': self.update.up_id
#         })
#         self.assertIsNotNone(new_job)
#         self.assertEqual(new_job.job_name, 'New Job')
#
#     def test_update_job(self):
#         now_time = datetime.utcnow()
#         updated_job_name = 'UPDATED test job name'
#         updated_job = Job.update_job(self.job.j_id, {
#             'j_id': None,
#             'job_name': updated_job_name,
#             'link': 'https://google.com/',
#             'frequency': '100',
#             'last_updated': now_time,
#             'next_update': now_time,
#             'p_id': '1',
#             's_id': '1',
#             'up_id': '1'
#         })
#         self.assertIsNotNone(updated_job)
#         self.assertEqual(updated_job.job_name, updated_job_name)
#
#     def test_delete_job(self):
#         deleted_job = Job.delete_job(self.job.j_id)
#         self.assertIsNotNone(deleted_job)
#         self.assertEqual(deleted_job.job_name, 'Test Job')
#
#     def test_get_all_profiles(self):
#         profiles = Profile.get_all_profiles()
#         self.assertIsNotNone(profiles)
#
#     def test_get_profile_by_id(self):
#         profile = Profile.get_profile_by_id(self.profile.p_id)
#         self.assertEqual(profile.email, 'test@test.com')
#
#     def test_create_profile(self):
#         new_profile = Profile.create_profile('new@test.com')
#         self.assertIsNotNone(new_profile)
#         self.assertEqual(new_profile.email, 'new@test.com')
#
#     def test_update_profile(self):
#         updated_profile = Profile.update_profile(self.profile.p_id, 'updated@test.com')
#         self.assertIsNotNone(updated_profile)
#         self.assertEqual(updated_profile.email, 'updated@test.com')
#
#     def test_delete_profile(self):
#         deleted_profile = Profile.delete_profile(self.profile.p_id)
#         self.assertIsNotNone(deleted_profile)
#         self.assertEqual(deleted_profile.email, 'test@test.com')
#
#     # def test_get_scraped_data(self):
#     #     scraped_data
