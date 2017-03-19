#!/usr/bin/env python

import random
import uuid

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


