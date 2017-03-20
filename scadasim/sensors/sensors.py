#!/usr/bin/env python

from scadasim.devices import Device
import logging

logging.basicConfig()
log = logging.getLogger()

# Sensors
class Sensor(Device):
    def __init__(self, worker_frequency=1, **kwargs):
        self.fluid = None
        super(Sensor, self).__init__(device_type="sensor", worker_frequency=worker_frequency, **kwargs)

    def output(self, to_device, volume):
        """Output used for pass-through sensors.
            If a connected device requests output, pass it upstream to the next device
        """
        available_volume = 0
        for i in self.inputs:
            available_volume = self.inputs[i].output(self, volume=volume)
        return available_volume

    def input(self, fluid, volume):
        """When fluid comes in, store the fluid context, and pass it downstream to all connected devices
        """
        self.fluid = fluid
        accepted_volume = 0
        for o in self.outputs:
            # Send the fluid on to all outputs
            #log.debug("%s sending fluid to %s" % (self, self.outputs[o]))
            accepted_volume = self.outputs[o].input(fluid, volume)
        return accepted_volume

    def worker(self):
        """Do something at `worker_frequency` rate
        """
        log.debug("%s fluid: %s" % (self, self.fluid))
        pass

    def read_sensor(self):
        """ Report sensor value
        """
        return self.fluid

class pHSensor(Sensor):
    def __init__(self, **kwargs):
        self.ph = None
        super(Sensor, self).__init__(device_type="sensor", worker_frequency=1, **kwargs)

    def input(self, fluid, volume):
        """When fluid comes in, store the fluid context, and pass it downstream to all connected devices
        """
        self.ph = fluid.ph

        log.debug("ph: ", self.ph)
        
        accepted_volume = 0
        for o in self.outputs:
            # Send the fluid on to all outputs
            #log.debug("%s sending fluid to %s" % (self, self.outputs[o]))
            accepted_volume = self.outputs[o].input(fluid, volume)
        return accepted_volume

    def read_sensor(self):
        """ Report sensor value
        """
        return self.ph
