#!/usr/bin/env python

import threading
import logging
import random
import uuid
from datetime import datetime

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Fluids
class Fluid(object):
    """Base class for all fluids
    """
    allowed_fluid_types = ['water']

    def __init__(self, fluid_type=None):
        self.uid = str(uuid.uuid4())[:8]
        self.fluid_type = fluid_type
        self.ph = None   					# For later use
        self.salinity = None                # For later use
        self.pressure = None                # For later use
        self.flowrate = None                # For later use

        if (not fluid_type) or (fluid_type not in self.allowed_fluid_types):
            raise InvalidFluid("\'%s\' in not a valid fluid type" % fluid_type)

    def __repr__(self):
        return """[%s][%s]
        	pH: %s
        	Salinity: %s
        	Pressure: %s
        	FlowRate: %s
        	""" % (self.uid, self.fluid_type, self.ph, self.salinity, self.pressure, self.flowrate)

    class InvalidFluid(Exception):
        """Exception handler for bad fluid types
        """
        def __init__(self, message):
            super(InvalidFluid, self).__init__(message)

class Water(Fluid):
    def __init__(self, **kwargs):
        super(Water, self).__init__(fluid_type='water', **kwargs)
        self.ph = round(random.uniform(6.5, 8.0), 2)


# Devices
class Device(object):

    allowed_device_types = ['pump', 'valve', 'tank', 'reservoir', 'filter', 'chlorinator']

    def __init__(self, device_type=None, fluid=None, label='', worker_frequency=1):
        self.uid = str(uuid.uuid4())[:8]
        self.device_type = device_type
        self.label = label
        self.inputs = {}
        self.outputs = {}
        self.fluid = fluid
        # Time interval in seconds. set to None if the device doesnt need a worker loop
        self.worker_frequency = worker_frequency

        if (not device_type) or (device_type not in self.allowed_device_types):
            raise InvalidDevice("\'%s\' in not a valid device type" % dev_type)

        #log.debug("%s initialized" % self)
        self.activate()

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
            threading.Timer(self.worker_frequency, self.activate).start()

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

    class InvalidDevice(Exception):
        """Exception thrown for bad device types
        """
        def __init__(self, message):
            super(InvalidDevice, self).__init__(message)


class Pump(Device):
    def __init__(self, state='off', **kwargs):
    	self.state = state
        super(Pump, self).__init__(device_type='pump', **kwargs)

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
    def __init__(self, state='closed', **kwargs):
    	self.state = state
        super(Valve, self).__init__(device_type="valve", worker_frequency=None, **kwargs)

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
    def __init__(self, volume=0, **kwargs):
    	self.volume = volume
        super(Tank, self).__init__(device_type="tank", **kwargs)

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
    def __init__(self, **kwargs):
    	self.device_type = 'reservoir'
        super(Reservoir, self).__init__(**kwargs)



"""
from devices import Water, Valve, Pump, Tank, Reservoir

water = Water()
reservoir1 = Reservoir(label="Reservoir1", fluid=water, volume=100000000)
tank2 = Tank(label="Tank2")
pump1 = Pump(label="Pump1")
valve1 = Valve(label="Valve1")
valve2 = Valve(label="Valve2")

reservoir1.add_output(valve1)
valve1.add_output(pump1)
pump1.add_output(valve2)
valve2.add_output(tank2)

valve1.open()
valve2.open()
pump1.turn_on()


water.ph = 5
"""

