"""
This file contains a test suite for the Device class.
"""
import pytest
from app.Device import Device

# Fixtures to create reusable Device instances used in later tests

@pytest.fixture
def device():
    """
    A generic device with default availability.
    Used to test basic instantiation.
    """
    return Device(1, 'NewDevice1', '192.168.0.1')

@pytest.fixture
def always_up():
    """
    A device with 100% availability.
    Used to test status generation and call behavior when always up.
    """
    return Device(2, 'NewDevice2', '192.168.0.2', avail=1)

@pytest.fixture
def always_down():
    """
    A device with 0% availability.
    Used to test status generation and call behavior when always down.
    """
    return Device(3, 'NewDevice3', '192.168.0.3', avail=0)

# Test cases for Device class behavior

def testConstructor(device):
    """
    Test that a Device object is instantiated correctly.
    """
    assert isinstance(device, Device)

def testConstructorInvalidID():
    """
    Test that passing a non-integer ID raises a TypeError.
    """
    with pytest.raises(TypeError):
        Device('ID1', 'Name1', '192.168.0.1')

def testConstructorKwarg():
    """
    Test that the optional 'avail' keyword argument is accepted and used.
    """
    assert isinstance(Device(1, 'Device', '127.0.0.1', avail=0.5), Device)

def testConstructorInvalidAvail():
    """
    Test that passing an invalid 'avail' value (>1) raises a ValueError.
    """
    with pytest.raises(ValueError):
        Device(1, 'Device', '127.0.0.1', avail=100)

def testConstructorInvalidAvailType():
    """
    Test that passing a non-float 'avail' value raises a ValueError.
    """
    with pytest.raises(ValueError):
        Device(1, 'Device', '127.0.0.1', avail='NotAFloat')

def testGenerateStatusUp(always_up):
    """
    Test that generateStatus returns True for a device with 100% availability.
    """
    assert always_up.generateStatus() is True

def testGenerateStatusDown(always_down):
    """
    Test that generateStatus returns False for a device with 0% availability.
    """
    assert always_down.generateStatus() is False

def testCallUp(always_up):
    """
    Test that calling a device with 100% availability returns expected status dictionary.
    """
    expected = {
        'id': 2,
        'name': "NewDevice2",
        'ip_address': "192.168.0.2",
        'status': True
    }
    assert always_up() == expected

def testCallDown(always_down):
    """
    Test that calling a device with 0% availability returns expected status dictionary.
    """
    expected = {
        'id': 3,
        'name': "NewDevice3",
        'ip_address': "192.168.0.3",
        'status': False
    }
    assert always_down() == expected
