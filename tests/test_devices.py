from scadasim.fluids import Water
from scadasim.devices import Valve, Pump, Tank, Reservoir

import time

def test_devices():
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

    reservoir1.activate()
    valve1.activate()
    pump1.activate()
    valve2.activate()

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
