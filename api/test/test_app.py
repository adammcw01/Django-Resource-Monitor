from app.app import generateDevices, app, main
from app.Device import Device
import unittest

class TestFlaskAPI(unittest.TestCase):
    """
    Test suite for Flask API, simulating network devices.
    """
    def setUp(self):
        """
        A helper method to create objects refered to in tests
        """
        app.devices = generateDevices(2, ["Router"], "192.168.0.")
        self.client = app.test_client()

    def test_FlaskResponse200(self):
        """
        Test that the Flask app running at localhost/devices returns a 200 status code.

         Asserts:
            bool: True if request responds with 200 (OK) status code.
        """
        response = self.client.get("/devices")
        self.assertEqual(response.status_code, 200)

    def test_FlaskResponse404(self):
        """
        Test that the Flask app running at localhost/invalid returns a 404 status code.

        Asserts:
            bool: True if request responds with 404 (not found) status code.
        """
        response = self.client.get("/invalid")
        self.assertEqual(response.status_code, 404)

    def test_ResponseNoDevices(self):
        """
        Test that the Flask app returns a 202 status code when no devices are available.

        Asserts:
            bool: True if request responds with 202 (empty) status code.
        """
        app.devices = []  # Empty device list
        response = self.client.get("/devices")
        self.assertEqual(response.status_code, 202)


    def test_MainTypeError(self):
        """
        Test that the method main raises a TypeError when an invalid argument is provided.

        Asserts:
            bool: True if raises TypeError.
        """
        with self.assertRaises(TypeError):
            main("not_a_number")

    def test_MainValueError(self):
        """
        Test that the method main raises a ValueError when a negative number of devices is provided.

        Asserts:
            bool: True if raises ValueError.
        """
        with self.assertRaises(ValueError):
            main("-1")

    def test_generateDevicesLength(self):
        """
        Test that the generateDevices function returns the correct number of devices.

        Asserts:
            bool: True if the number of devices is the same as expected.
        """
        devices = generateDevices(3, ["Router"], "192.168.0.")
        self.assertEqual(len(devices), 3)
    
    def test_generateDevicesType(self):
        """
        Test that the generateDevices function returns a list of Device objects.
                
        Asserts:
            bool: True if the returned devices are all instances of Device.
        """
        devices = generateDevices(3, ["Router"], "192.168.0.")
        self.assertTrue(all(isinstance(d, Device) for d in devices))
    
    def test_generateDeviceUnique(self):
        """
        Test that the generateDevices function returns devices with unique IDs.

        Asserts:
            bool: True if all device IDs are unique.
        """
        devices = generateDevices(5, ["Device"], "10.0.0.")  # Generate 5 devices
        ids = [d()['id'] for d in devices] # Call each device as Dict and parse ID
        # If length of collection and length of set of collection are equal, items are unique.
        self.assertEqual(len(ids), len(set(ids)))