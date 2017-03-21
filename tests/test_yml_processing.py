from scadasim.utils import parse_yml, build_simulation

def test_yml_processing():

    config = parse_yml('tests/test_water_plant.yml')
    simulation = build_simulation(config)
    settings = simulation['settings']
    devices = simulation['devices']
    sensors = simulation['sensors']

    print settings
    print devices

    # Disable the workers
    for device_label in devices:
        devices[device_label].worker_frequency=None

    assert devices['valve2'].uid in devices['tank1'].inputs
    assert devices['pump1'].uid in devices['valve2'].inputs
    assert devices['valve1'].uid in devices['pump1'].inputs
    assert devices['reservoir1'].uid in devices['valve1'].inputs
    assert not devices['reservoir1'].inputs
