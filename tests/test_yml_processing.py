from scadasim.utils import parse_yml

def test_yml_processing():
    config = parse_yml('tests/test_water_plant.yml')
    devices = {}

    print config

    # Process devices
    for device in config['devices']:
        devices[device.label] = device

        if device.label == 'reservoir1':
            print device.fluid

    # process connections
    for device_label, connections in config['connections'].iteritems():
        if 'outputs' in connections:
            for dev_output in connections['outputs']:
                print "%s -> %s" % (device_label, dev_output)
                devices[device_label].add_output(devices[dev_output])
        if 'inputs' in connections:
            for dev_input in connections['inputs']:
                print "%s -> %s" % (dev_input, device_label)
                devices[device_label].add_input(devices[dev_input])

    # Disable the workers
    for device_label in devices:
        devices[device_label].worker_frequency=None


    assert devices['valve2'].uid in devices['tank1'].inputs
    assert devices['pump1'].uid in devices['valve2'].inputs
    assert devices['valve1'].uid in devices['pump1'].inputs
    assert devices['reservoir1'].uid in devices['valve1'].inputs
    assert not devices['reservoir1'].inputs