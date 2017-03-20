#!/usr/bin/env python

import threading
import logging
import uuid
from datetime import datetime
import yaml

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class InvalidDevice(Exception):
        """Exception thrown for bad device types
        """
        def __init__(self, message):
            super(InvalidDevice, self).__init__(message)

# Devices
class Device(yaml.YAMLObject):
    allowed_device_types = ['pump', 'valve', 'tank', 'reservoir', 'filter', 'chlorinator', 'sensor']

    def __init__(self, device_type=None, fluid=None, label='', worker_frequency=1):
        self.uid = str(uuid.uuid4())[:8]
        self.device_type = device_type
        self.label = label
        self.inputs = {}
        self.outputs = {}
        self.fluid = fluid
        # Time interval in seconds. set to None if the device doesnt need a worker loop
        self.worker_frequency = worker_frequency

        if (not self.device_type) or (self.device_type not in self.allowed_device_types):
            raise InvalidDevice("\'%s\' in not a valid device type" % self.device_type)

        #log.debug("%s initialized" % self)
        #self.activate()

    @classmethod
    def from_yaml(cls, loader, node):
        fields = loader.construct_mapping(node, deep=False)
        return cls(**fields)

    def add_input(self, device):
        """Add the connected `device` to our inputs and add this device to the connected device's outputs
        """
        if device.uid not in self.inputs:
            self.inputs[device.uid] = device
            device.add_output(self)

    def add_output(self, device):
        """Add the connected device to our outputs and add this device to connected device's inputs
        """
        if device.uid not in self.outputs:
            self.outputs[device.uid] = device
            device.add_input(self)

    def activate(self):
        """Executed at atleast once and at regular intervals if `worker_frequency` is not None.
            Used to call worker method
        """
        #log.debug("%s %s activated" % (datetime.now().time(), self))
        self.worker()
        if self.worker_frequency:
            t = threading.Timer(self.worker_frequency, self.activate)
            t.daemon = True
            t.start()

    def worker(self):
        """Do something each cycle of `worker_frequency`
            Update fluid, pull inputs, push outputs, etc.
            Override this for each custom Device
        """
        pass

    def input(self, fluid):
        """Receive and process some fluid
            Override this with your own processing to perform when new fluid is received
        """
        return 0

    def output(self):
        """Receive and process some fluid
            Override this with your own processing to perform when fluid is outputted
        """
        return 0

    def __repr__(self):
        return "[%s][%s][%s]" % (self.uid, self.device_type, self.label)


class Pump(Device):
    yaml_tag = u'!pump'

    def __init__(self, state='off', device_type='pump', **kwargs):
    	self.state = state
        super(Pump, self).__init__(device_type=device_type, **kwargs)

    def worker(self):
        """Manipulate the fluid just as this device would in the real world
        """
        #log.debug("%s worker" % self)
        if self.state == 'off':
            # Pump is off, do nothing
            #log.debug("%s Pump is off" % self)
            pass

        elif self.state == 'on':
            # Pump is on
            for i in self.inputs:
                #log.debug("%s Getting input from %s" % (self, self.inputs[i]))
                # Draw from all inputs inputs
                self.inputs[i].output(self)

    def input(self, fluid, volume=1):
        if self.state == 'on':
            self.fluid = fluid
            for o in self.outputs:
                # Send fluid to all outputs
                accepted_volume = self.outputs[o].input(fluid, volume)
            return accepted_volume
        else:
            return 0

    def output(self, to_device, volume=1):
        if self.state == 'on':
            return self.fluid
        else:
            return 0

    def turn_on(self):
        self.state = 'on'

    def turn_off(self):
        self.state = 'off'


class Valve(Device):
    yaml_tag = u'!valve'

    def __init__(self, state='closed', device_type='valve', **kwargs):
    	self.state = state
        super(Valve, self).__init__(device_type=device_type, worker_frequency=None, **kwargs)

    def open(self):
        self.state = 'open'

    def close(self):
        self.state = 'closed'

    def output(self, to_device, volume=1):
        """If the valve is open, pull `volume` amount from connected devices
            TODO: Handle multiple inputs and outputs. Distributing the volume across
            all based on valve capacity.
        """
        if self.state == 'open':
            available_volume = 0
            for i in self.inputs:
                available_volume = self.inputs[i].output(self, volume=volume)
            return available_volume
        else:
            #log.debug("%s closed" % self)
            return 0

    def input(self, fluid, volume=1):
        """If the valve is open, pass `volume` amount of `fluid` to the connected devices
            Normally used when pump's push fluid through.
        """
        if self.state == 'open':
            accepted_volume = 0
            for o in self.outputs:
                # Send the fluid on to all outputs
                #log.debug("%s sending fluid to %s" % (self, self.outputs[o]))
                accepted_volume = self.outputs[o].input(fluid, volume)
            return accepted_volume
        else:
            return 0


class Tank(Device):
    yaml_tag = u'!tank'

    def __init__(self, volume=0, device_type='tank', **kwargs):
    	self.volume = volume
        super(Tank, self).__init__(device_type=device_type, **kwargs)

    def __increase_volume(self, volume):
        """Raise the tank's volume by `volume`"""
        self.volume += volume
        return volume

    def __decrease_volume(self, volume):
        """Lower the tank's volume by `volume`"""
        self.volume -= self.__check_volume(volume)

    def __check_volume(self, volume):
        """See if the tank has enough volume to provide the requested `volume` amount
        """
        if self.volume <= 0:
            volume = 0
        elif self.volume > volume:
            volume = volume
        else:
            volume = self.volume
        return volume

    def __update_fluid(self, new_context):
    	self.fluid = new_context

    def input(self, fluid, volume=1):
        """Receive `volume` amount of `fluid`"""
        self.__update_fluid(fluid)
        accepted_volume = self.__increase_volume(volume)
        return accepted_volume

    def output(self, to_device, volume=1):
        """Send `volume` amount of fluid to connected device
            This verifies that the connected device accepts the amount of volume before
            we decrease our volume. e.g. full tank.
        """
        accepted_volume = to_device.input(self.fluid, self.__check_volume(volume))
        self.__decrease_volume(accepted_volume)

    def worker(self):
        """For debugging only. Used to display the tank's volume"""
        log.debug("%s volume: %s" % (self, self.volume))
        log.debug(self.fluid)
        pass


class Reservoir(Tank):
    yaml_tag = u'!reservoir'

    def __init__(self, **kwargs):
        super(Reservoir, self).__init__(device_type='reservoir', **kwargs)


