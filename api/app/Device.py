"""
Device.py

This module provides a class to simulate a network device.
This device can be used to test a system monitoring the health of devices.

Classes:
    Device: A simulated network device.

"""

from typing import Dict, Union
from random import uniform
import json

class Device:
    """
    A generic network enabled device.

    Attributes:
        id (int): The unique identifier for this device.
        name (str): A user friendly name to identify this device.
        ipAddress (str): This devices own address.
        isAwake (bool): The current status of the device.
            (True is up, False is Down)
        Availability (float): A value between 0 and 1 representing a devices expected availability.
    """
    def __init__(self, id: int, name: str, ipAddress: str, **kwargs: Dict[str, float]) -> None:
        """
        Constructor for the Device object.

        Args:
            id (int): The unique identifier for this device.
            name (str): A user friendly name to identify this device.
            ipAddress (str): This devices own address.
            **kwargs:
                Keyword Arguments:
                avail (float): A value between 0 and 1 representing a devices expected availability.

        Returns:
            None
        
        Raises:
            ValueError: If Keyword Availability is named and outside of range 0-1.
        """
        
        avail: float = kwargs.get('avail', uniform(0.8, 1))
        if isinstance(avail, float):
            if ((avail > 1) or (avail < 0)):
                raise ValueError(f'Attempted to create a device with {round(avail*100)}% availability.')
        else:
            avail: float = uniform(0.8, 1) # If avail is invalid type assign random availability

        self.__id: int = id
        self.__name: str = name
        self.__ipAddress: str = ipAddress
        self.__availability: float = avail
        self.__isAwake: bool = self.generateStatus()

    def generateStatus(self) -> bool:
        """
        Randomly generate if a device is up or down based on its expected availability.

        Args:
            None
        
        Returns:
            bool: The status of the device based on a random chance.
        """
        roll: float = uniform(0, 1) # generate random value.
        if roll > self.__availability: # If value is higher than availability, device is down.
            return False
        return True


    def __call__(self) -> Dict[str, Union[int, str, bool]]:
        """
        Overloader for the inbuilt call method.
        Generates a Python Dictionary for the devices status.
        Simulating the device getting a generic request.

        Args:
            None
        
        Returns:
            Dict[str, (int|str|bool)]: The current device information.
        """
        deviceInfo: Dict[str, Union[int, str, bool]] = {
            'id': self.__id,
            'name': self.__name,
            'ip_address': self.__ipAddress,
            'status': self.generateStatus()
        }
        return deviceInfo
    
    def __repr__(self):
        """
        Generate a JSON string for the devices status.
        Simulating the device getting a generic request.

        Args:
            None
        
        Returns:
            str: A JSON string for the current status of the device.
        """
        return json.dumps(self())