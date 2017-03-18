#!/usr/bin/env python

import random
import uuid
import yaml
import logging

log = logging.getLogger('scadasim')

# Fluids
class Fluid(yaml.YAMLObject):
    """Base class for all fluids
    """
    allowed_fluid_types = ['water', 'chlorine']

    def __init__(self, fluid_type=None, ph=None, temperature=None, salinity=None, pressure=None, flowrate=None):
        self.uid = str(uuid.uuid4())[:8]
        self.fluid_type = fluid_type
        self.ph = ph   					# For later use
        self.temperature = temperature  # For later use
        self.salinity = salinity        # For later use
        self.pressure = pressure        # For later use
        self.flowrate = flowrate        # For later use

        if (not fluid_type) or (fluid_type not in self.allowed_fluid_types):
            raise InvalidFluid("\'%s\' in not a valid fluid type" % fluid_type)

    def __repr__(self):
        return """[%s][%s]
        	pH: %s
        	Salinity: %s
        	Pressure: %s
        	FlowRate: %s
        	""" % (self.uid, self.fluid_type, self.ph, self.salinity, self.pressure, self.flowrate)

    @classmethod
    def from_yaml(cls, loader, node):
        fields = loader.construct_mapping(node, deep=False)
        return cls(**fields)

    class InvalidFluid(Exception):
        """Exception handler for bad fluid types
        """
        def __init__(self, message):
            super(InvalidFluid, self).__init__(message)

class Water(Fluid):
    yaml_tag = u'!water'

    def __init__(self, **kwargs):
        super(Water, self).__init__(fluid_type='water', **kwargs)
        self.ph = round(random.uniform(6.5, 8.0), 2)

class Chlorine(Fluid):
    yaml_tag = u'!chlorine'

    def __init__(self, **kwargs):
        super(Chlorine, self).__init__(fluid_type='chlorine', **kwargs)
        self.ph = 5

