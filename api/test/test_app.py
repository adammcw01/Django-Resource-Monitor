from app.Device import Device
import unittest
from app import app
import json

class FlaskAppTestCase(unittest.TestCase):
    """
    Test suite for flask app to serve simulated network devices.
    """
    def setUp(self):
        # Creates a test client
        self.client = app.test_client()
        # Propagate exceptions to the test client
        app.testing = True

    def testGetDeviceStatus(self):
        """
        Test that the app responds to a GET request at /devices.
        """
        response = self.client.get('/devices')
        self.assertEqual(response.status_code, 200)

    def testGetDeviceStatus(self):
        """
        Test the when requested 4 devices are returned.
        """
        response = self.client.get('/devices')
        reply = json.loads(response.reply)
        self.assertEqual(len(reply), 4)