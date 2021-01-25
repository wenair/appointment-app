import unittest
import json

from gateway import app

class BasicTestCase(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')

    def test_endpoints_that_donot_exist(self):
        tester = app.test_client(self)
        response = tester.get('random', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_appointments_that_dont_exist(self):
        tester = app.test_client(self)
        response = tester.get('appointments/Tom', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Found no appointments' in response.data)

    def test_create_appointment_with_no_date_throws_error(self):
        tester = app.test_client(self)
        response = tester.post('appointments/Jeff', data=json.dumps(dict(somekey='somedata')), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'ERROR: No datetime passed in' in response.data)

    def test_create_appointment_with_bad_date_throws_error(self):
        tester = app.test_client(self)
        response = tester.post('appointments/Jeff', data=json.dumps(dict(datetime='somedata')), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'ERROR: Datetime has to be of format' in response.data)

    def test_create_appointment_with_same_date_as_existing_entry_throws_error(self):
        tester = app.test_client(self)
        response = tester.post('appointments/Jeff', data=json.dumps(dict(datetime='2021-01-24 14:00')), content_type='application/json')
        response = tester.post('appointments/Jeff', data=json.dumps(dict(datetime='2021-01-24 10:00')), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'ERROR: Appointment already exists for date.' in response.data)

    #Tests both post and get. Did not find a good way to test post without the get
    def test_create_appointment_with_good_date_has_no_error(self):
        tester = app.test_client(self)
        response = tester.post('appointments/Jeff', data=json.dumps(dict(datetime='2021-01-24 14:00')), content_type='application/json')
        response = tester.post('appointments/Jeff', data=json.dumps(dict(datetime='2021-01-22 14:00')), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = tester.get('appointments/Jeff', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Found 2 appointment(s)' in response.data)
        
if __name__ == '__main__':
    unittest.main()
