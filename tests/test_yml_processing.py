import yaml
import json
import time

from scadasim.fluids import Water
from scadasim.devices import Valve, Pump, Tank, Reservoir
import scadasim

def parse_yml(path_to_tml_file):
    stream = file(path_to_yml_file, 'r')
    config = yaml.load(stream)
    return config

def process_config(config):
    print json.dumps(config, indent=4)

    devices = {}

    for device in config:
        dev_type = config[device]['type']
        dev_label = config[device]['label']
        dev_class_ = None

        try:
            dev_class_ = getattr(scadasim.fluids, dev_type.capitalize())
        except:
            try:
                dev_class_ = getattr(scadasim.devices, dev_type.capitalize())
            except:
                try:
                    dev_class_ = getattr(scadasim.sensors, dev_type.capitalize())
                except:
                    pass
    
        if dev_class_:
            instance = dev_class_(type=dev_type, label=dev_label)
            devices[instance.uid] = {'device': instance, 'config': config}

    for device in devices:
        

def test_yml_processing():

    config = parse_yml('tests/water_plant.yml')
    process_config(config)

    assert False    


    """
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

    time.sleep(5)

    pump1.turn_off()
    valve1.close()
    valve2.close()

    reservoir1.worker_frequency=None
    tank2.worker_frequency=None
    pump1.worker_frequency=None

    assert reservoir1.fluid == tank2.fluid
    """
