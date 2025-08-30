from app.Device import Device
import unittest

class TestSimDevice(unittest.TestCase):
    """
    Test suite for Device class.
    """
    def setUp(self):
        """
        A helper method to create objects refered to in tests
        """
        self.device = Device(1, 'NewDevice1', '192.168.0.1')
        self.alwaysUp = Device(2, 'NewDevice2', '192.168.0.2', avail=1)
        self.alwaysDown = Device(3, 'NewDevice3', '192.168.0.3', avail=0)

    def testConstructor(self):
        """
        Test the instanciation of the object.

        Asserts:
            bool: True if object is created successfully.
        """
        self.assertIsInstance(self.device, Device)

    def testConstructorInvalidID(self):
        """
        Test the instanciation of the object if ID is not an integer.

        Asserts:
            bool: True if object raises TypeError.
        """
        with self.assertRaises(TypeError):
           Device('ID1', 'Name1', '192.168.0.1')

    def testConstructorKwarg(self):
        """
        Test class constructor when passing the optional keyword argument `avail`.

        Asserts:
            bool: True if object created successfully
        """
        self.assertIsInstance(Device(1, 'Device', '127.0.0.1', avail=0.5), Device)


    def testConstructorInvalidAvail(self):
        """
        Test that the instanciation of the object fails.
        When the optional keyword `avail` is passed and invalid

        Asserts:
            bool: True if contrsuctor raises ValueError.
        """
        with self.assertRaises(ValueError):
            Device(1, 'Device', '127.0.0.1', avail=100)

    def testConstructorAvailBadType(self):
        """
        Test that the instanciation of the object fails.
        When the optional keyword `avail` is passed is an invalid type.

        Asserts:
            bool: True if contrsuctor raises TypeError.
        """
        with self.assertRaises(ValueError):
            Device(1, 'Device', '127.0.0.1', avail='NotAFloat')

    def testGenerateStatusUp(self):
        """
        Test the generateStatus method returns True when a device has 100% availability
        """
        self.assertTrue(self.alwaysUp.generateStatus())

    
    def testGenerateStatusDown(self):
        """
        Test the generateStatus method returns False when a device has 0% availability
        """
        self.assertFalse(self.alwaysDown.generateStatus())

    def testCallUp(self):
        """
        Test that the overloaded call method returns the expected dictionary,
        when the device has 100 availability.
        """
        actual = self.alwaysUp()
        expected = {
            'id': 2,
            'name': "NewDevice2",
            'ip_address': "192.168.0.2",
            'status': True
        }
        self.assertEqual(expected, actual)

    def testCallDown(self):
        """
        Test that the overloaded call method returns the expected dictionary,
        when the device has 100 availability.
        """
        actual = self.alwaysDown()
        expected = {
            'id': 3,
            'name': "NewDevice3",
            'ip_address': "192.168.0.3",
            'status': False
        }
        self.assertEqual(expected, actual)