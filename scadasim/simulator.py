import threading
from scadasim.utils import parse_yml, build_simulation
import sys
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Simulator(object):

    def __init__(self, dbus=False):
        self.dbus = dbus
        if self.dbus:
            from dbusservice import DBusService
            self.dbusservice = DBusService()

    def load_yml(self, path_to_yaml_config):
        """Read and parse YAML configuration file into simulator devices
        """
        self.path_to_yaml_config = path_to_yaml_config
        self.config = parse_yml(path_to_yaml_config)
        simulation = build_simulation(self.config)
        self.settings = simulation['settings']
        self.devices = simulation['devices']
        self.sensors = simulation['sensors']
        self.plcs = simulation['plcs']

        self.set_speed(self.settings['speed'])

    def start(self):
        """Start the simulation"""
        for device in self.devices.values():
            device.activate()

        for sensor in self.sensors.values():
            sensor.activate()

        if self.dbus:
            for plc in self.plcs:
                for sensor in self.plcs[plc]['sensors']:
                	log.debug(self.sensors)
                    self.plcs[plc][sensor]['read_sensor'] = self.sensors[sensor].read_sensor
            self.dbusservice.load_plcs(self.plcs)
            self.dbusservice.set_speed(self.settings['speed'])
            self.dbusservice.activate()

    def pause(self):
        """Pause the simulation"""
        for device in self.devices.values():
            device.deactivate()

        for sensor in self.sensors.values():
            sensor.deactivate()

        if self.dbus:
            self.dbusservice.deactivate()

    def stop(self):
        """Stop and destroy the simulation"""
        self.pause()
        sys.exit(0)

    def set_speed(self, speed):
        """Increase/Decrease the speed of the simulation
            default: 1/second
        """
        for device in self.devices.values():
            device.speed = speed

        for sensor in self.sensors.values():
            sensor.speed = speed

        if self.dbus:
            self.dbusservice.set_speed(speed)

    def restart(self):
        """Stop and reload the simulation from the original config"""
        self.pause()
        self.load_yml(self.path_to_yaml_config)
        self.start()