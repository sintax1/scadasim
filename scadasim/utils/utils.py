import yaml

from scadasim.fluids import *
from scadasim.devices import *
from scadasim.sensors import *

def parse_yml(path_to_yml_file):
    config = None
    with open(path_to_yml_file, 'r') as stream:
        config = yaml.load(stream)
    return config
