import argparse
from typing import List, Dict
from Device import Device
from flask import Flask, Response, current_app
from random import choice
import sys
import json

app = Flask(__name__)

@app.route("/devices", methods=["GET"])
def getStatus()->Response:
    """
    Query the status of all devices.
    Returns the status as a JSON string.

    Args:
        None

    Returns:
        flask.Response: The HTTP response to forward to the client.
    """
    devices: List[Device] = current_app.devices # Get devices from setup phase.
    status: List[Dict[str, (int|bool|str)]] = [device() for device in devices] # Get status of each device.

    reply: str = json.dumps(status)

    if reply == 'null': # Handle case where device list is empty.
        response: Flask.Response = Response(
            response='{Error: No Devices Found}',
            status=202,
            mimetype='application/json'
        )
    elif reply:
        response: Flask.Response = Response( # Expected Case
            response=reply,
            status=200,
            mimetype='application/json'
        )
    else:
        response: Flask.Response = Response( # Case when reply is empty 
            response='{Error: Internal Server Error}',
            status=500,
            mimetype='application/json'
        )
    return response

def generateDevices(NUM_DEVICES: int, NAMES: List[str], IP_PREFIX: str)->List[Device]:
    """
    Randomly generate a list of devices.

    Args:
        NUM_DEVICES (int): Number of devices to generate.
        NAMES: A list of random device types to prefix the device name with.
        IP_PREFIX: The prefix for the ip address range.
    
    Returns:
        List[Device]: A list of generated Device objects.
    """
    devices: List[Device] = [
        Device(id=i, name=f'{choice(NAMES)}_{i}', ipAddress=f'{IP_PREFIX}{i}')
        for i in range(NUM_DEVICES)
        ]
    
    return devices


def main(NUM_DEVICES: str)->int:

    try:
        NUM_DEVICES: int = int(NUM_DEVICES)
    except ValueError:
        raise ValueError('Number of devices must be an integer.')

    NAMES: List[str] = ['Router', 'Switch', 'Phone', 'Firewall', 'PC'] # Default Prefixes for device names.
    IP_PREFIX: str = '192.168.0.' # IP address range for devices.

    devices = generateDevices(NUM_DEVICES, NAMES, IP_PREFIX)
    
    app.devices = devices # Add devices to Flask  app environment.

    app.run(host="127.0.0.1", port=8000)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--devices', nargs='?', default=4)
    args = parser.parse_args()

    status: int = main(args.devices)
    sys.exit(status)
