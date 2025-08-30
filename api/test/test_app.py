"""
This file contains the test suite for a Flask API that simulates network devices.
"""
import pytest
from app.app import generateDevices, app, main
from app.Device import Device

# Fixture to initialize Flask test client and attach devices to the app.

@pytest.fixture
def client():
    """
    Creates a Flask test client with two simulated devices.
    """
    app.devices = generateDevices(2, ["Router"], "192.168.0.")
    return app.test_client()

# Flask route tests

def testFFlaskResponse200(client):
    """
    Test that the Flask app running at localhost/devices returns a 200 (OK) status code.
    """
    response = client.get("/devices")
    assert response.status_code == 200

def testFlaskResponse404(client):
    """
    Test that the Flask app running at /invalid returns a 404 (Not Found) status code.
    """
    response = client.get("/invalid")
    assert response.status_code == 404

def testFlaskResponseNoDevices(client):
    """
    Test that the Flask app returns a 202 (Empty) status code when no devices are available.
    """
    app.devices = []  # Empty device list
    client = app.test_client()
    response = client.get("/devices")
    assert response.status_code == 202

# Main function error handling tests

def testMainTypeError():
    """
    Test that the main function raises a TypeError when an invalid argument is provided.
    """
    with pytest.raises(TypeError):
        main("NotANumber")

def testMainValueError():
    """
    Test that the main function raises a ValueError when a negative number of devices is provided.
    """
    with pytest.raises(ValueError):
        main("-1")

# Device generation logic tests

def testGenerateDevicesLength():
    """
    Test that generateDevices returns the expected number of devices.
    """
    devices = generateDevices(3, ["Router"], "192.168.0.")
    assert len(devices) == 3

def testGenerateDevicesType():
    """
    Test that generateDevices returns a list of Device objects.
    """
    devices = generateDevices(3, ["Router"], "192.168.0.")
    assert all(isinstance(d, Device) for d in devices)

def testGenerateDevicesUniqueIDs():
    """
    Test that generateDevices returns devices with unique IDs.
    """
    devices = generateDevices(5, ["Device"], "10.0.0.")  # Generate 5 devices
    ids = [d()['id'] for d in devices] # Call each device as Dict and parse ID
    # If length of collection and length of set of collection are equal, items are unique.
    assert len(ids) == len(set(ids))  # IDs should be unique