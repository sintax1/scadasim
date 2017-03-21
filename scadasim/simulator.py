import threading
from scadasim.utils import parse_yml, build_simulation
import sys
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Simulator(object):

	def load_yml(self, path_to_yaml_config):
		"""Read and parse YAML configuration file into simulator devices
		"""
		self.path_to_yaml_config = path_to_yaml_config
		self.config = parse_yml(path_to_yaml_config)
		simulation = build_simulation(self.config)
		self.settings = simulation['settings']
		self.devices = simulation['devices']
		self.sensors = simulation['sensors']

		self.set_speed(self.settings['speed'])

	def start(self):
		"""Start the simulation"""
		for device in self.devices.values():
			device.activate()

		for sensor in self.sensors.values():
			sensor.activate()

	def pause(self):
		"""Pause the simulation"""
		for device in self.devices.values():
			device.deactivate()

		for sensor in self.sensors.values():
			sensor.deactivate()

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

	def restart(self):
		"""Stop and reload the simulation from the original config"""
		self.pause()
		self.load_yml(self.path_to_yaml_config)
		self.start()