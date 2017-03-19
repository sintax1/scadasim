# scada-simulator
SCADA Simulator encompassing things from PLCs to devices such as valves, pumps, tanks, etc. and environmental properties such as water pH levels

## Installation
```bash
$ git clone https://github.com/sintax1/scadasim.git
$ cd scadasim
$ pip install .
```

## Usage
```python
from scadasim.devices import Water, Valve, Pump, Tank, Reservoir

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
```

## TODO
Working on adding the sensors that will connect to the devices, which will eventually connect to the PLC simulators.
