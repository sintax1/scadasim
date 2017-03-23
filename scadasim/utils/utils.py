import yaml

from scadasim.fluids import *
from scadasim.devices import *
from scadasim.sensors import *

def parse_yml(path_to_yml_file):
    config = None
    with open(path_to_yml_file, 'r') as stream:
        config = yaml.load(stream)
    return config

def build_simulation(config):
    settings = config['settings']
    devices = {}
    sensors = {}
    plcs = {}

    # Process devices
    for device in config['devices']:
        devices[device.label] = device

    # process connections
    for device_label, connections in config['connections'].iteritems():
        if 'outputs' in connections:
            for dev_output in connections['outputs']:
                devices[device_label].add_output(devices[dev_output])
        if 'inputs' in connections:
            for dev_input in connections['inputs']:
                devices[device_label].add_input(devices[dev_input])

    # process sensors
    for sensor in config['sensors']:
        device_to_monitor = devices[sensor.device_to_monitor]
        sensor.monitor_device(device_to_monitor)
        sensors[sensor.label] = sensor

    # process PLCs
    plcs = config['plcs']
    for plc in plcs:
        # Add registered state so we can tell if the PLC has communicated with the sensors
        plcs[plc]['registered'] = False
        # Add all sensor.read_sensor connections to each plc
        for sensor in plcs[plc]['sensors']:
            plcs[plc]['sensors'][sensor]['value'] = 0
            plcs[plc]['sensors'][sensor]['read_sensor'] = sensors[sensor].read_sensor

    return {'settings': settings, 'devices': devices, 'sensors': sensors, 'plcs': plcs}
