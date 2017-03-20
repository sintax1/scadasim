# scada-simulator
SCADA Simulator encompassing things from PLCs to devices such as valves, pumps, tanks, etc. and environmental properties such as water pH levels

## Requirements
   * python-pip

## Installation
```bash
$ git clone https://github.com/sintax1/scadasim.git
$ cd scadasim
$ make
```
## Running Tests
```bash
$ make test
```
## Running a simulation using a configuration file
```bash
# Run default config
$ make run
-Or-
# Run custom config
$ python -i run.py -c [YAML config]
INFO:root:[e660148d][reservoir][reservoir1]: Initialized
INFO:root:[0efd0900][valve][valve1]: Initialized
INFO:root:[db91f04a][pump][pump1]: Initialized
INFO:root:[1d81d76b][valve][valve2]: Initialized
INFO:root:[f41bb0d9][tank][tank1]: Initialized
INFO:root:[0efd0900][valve][valve1]: Added input <- [e660148d][reservoir][reservoir1]
INFO:root:[e660148d][reservoir][reservoir1]: Added output -> [0efd0900][valve][valve1]
INFO:root:[db91f04a][pump][pump1]: Added input <- [0efd0900][valve][valve1]
INFO:root:[0efd0900][valve][valve1]: Added output -> [db91f04a][pump][pump1]
INFO:root:[f41bb0d9][tank][tank1]: Added input <- [1d81d76b][valve][valve2]
INFO:root:[1d81d76b][valve][valve2]: Added output -> [f41bb0d9][tank][tank1]
INFO:root:[1d81d76b][valve][valve2]: Added input <- [db91f04a][pump][pump1]
INFO:root:[db91f04a][pump][pump1]: Added output -> [1d81d76b][valve][valve2]
INFO:root:[1d81d76b][valve][valve2]: Active
INFO:root:[f41bb0d9][tank][tank1]: Active
INFO:root:[0efd0900][valve][valve1]: Active
INFO:root:[e660148d][reservoir][reservoir1]: Active
INFO:root:[db91f04a][pump][pump1]: Active
>>> sim.devices
{'valve2': [1d81d76b][valve][valve2], 'tank1': [f41bb0d9][tank][tank1], 'valve1': [0efd0900][valve][valve1], 'reservoir1': [e660148d][reservoir][reservoir1], 'pump1': [db91f04a][pump][pump1]}
>>> sim.settings
{'speed': 1}
>>> sim.devices['tank1'].volume
79
>>> sim.devices['pump1'].turn_off()
>>> sim.devices['tank1'].volume
103
>>> sim.devices['tank1'].volume
103
>>> sim.pause()
INFO:root:[dd153bbb][valve][valve2]: Inactive
INFO:root:[16960a58][tank][tank1]: Inactive
INFO:root:[d4d9302d][valve][valve1]: Inactive
INFO:root:[a2f02e65][reservoir][reservoir1]: Inactive
INFO:root:[f1afd77b][pump][pump1]: Inactive
>>> sim.start()
INFO:root:[dd153bbb][valve][valve2]: Active
INFO:root:[16960a58][tank][tank1]: Active
INFO:root:[d4d9302d][valve][valve1]: Active
INFO:root:[a2f02e65][reservoir][reservoir1]: Active
INFO:root:[f1afd77b][pump][pump1]: Active
>>> sim.stop()
$
```
### Example YAML Config
```yaml
settings:
  speed: 1

devices:
  - !reservoir
    label: reservoir1
    volume: 1000
    fluid: !water {}
  - !valve
    label: valve1
    state: 'open'
  - !pump
    label: pump1
    state: 'on'
  - !valve
    label: valve2
    state: 'open'
  - !tank
    label: tank1

connections:
  reservoir1:
    outputs: 
     - valve1
  valve1:
    outputs:
     - pump1
  pump1:
    outputs:
     - valve2
  valve2:
    outputs:
     - tank1
```

## Running a simulation within your own python script
```python
# Import a fluid with properties
from scadasim.fluids import Water
# Import the devices
from scadasim.devices import Valve, Pump, Tank, Reservoir

# Instantiate the fluid and devices
water = Water()
reservoir1 = Reservoir(label="Reservoir1", fluid=water, volume=100000000)
tank2 = Tank(label="Tank2")
pump1 = Pump(label="Pump1")
valve1 = Valve(label="Valve1")
valve2 = Valve(label="Valve2")

# Connect the devices
reservoir1.add_output(valve1)
valve1.add_output(pump1)
pump1.add_output(valve2)
valve2.add_output(tank2)

# Activate the devices
reservoir1.activate()
valve1.activate()
pump1.activate()
valve2.activate()

# Manipulate the devices
valve1.open()
valve2.open()
pump1.turn_on()
```

## Extending the simulator by adding your own device, sensor, or fluid
```python
from scadasim.devices import Device

class MyCustomDevice(Device):
    yaml_tag = u'!mycustomdevice' # So it can be used within YAML configs
    
    def __init__(self, myvariable=0, **kwargs):
        # Add your custom variables here
        self.myvariable = myvariable
        super(MyCustomDevice, self).__init__(device_type="tank", **kwargs)

    def input(self, fluid, volume):
        """Receive `volume` amount of `fluid` and return the amount your device is willing to receive
            accepted_volume = 0: Don't accept any fluid
            accepted_volume = volume: Accept it all
            accepted_volume = volume / 2: Restrict flow by accepting a fraction of the volume
        """
        ...
        Do something here with the fluid that the connected devices send to your device's input
        ...
        return accepted_volume

    def output(self, to_device, volume):
        """ `to_device` is pulling this device's output (sucking fluid) in the mount of `volume`
        """
        # If you accept the request, send the fluid to the requesting devices input
        accepted_volume = to_device.input(self.fluid, volume)

    def worker(self):
        """Do something each cycle of `worker_frequency`
            Update fluid, pull inputs, push outputs, etc.
            If your device only performs work based on input and output stimulation, 
            there may be no need to have this worker. Such as a valve.
        """
        pass
        
# Use it
mydevice = MyCustomDevice(fluid=water, myvariable=10) 
        
```
