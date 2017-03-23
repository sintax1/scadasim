#!/usr/bin/env python

from scadasim import Simulator

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Build and run SCADA simulated environments')
	parser.add_argument('-c', '--config', help='YAML configuration file to load', required=True)
	parser.add_argument('-d', '--dbus', help='Connect to dbus to communicate with scadasim PLCs', action='store_true')
	args = parser.parse_args()

	sim = Simulator()
	sim.load_yml(args.config)

    if args.dbus:
        from dbusservice import DBusService
        d = DBusService()
        d.start()

	sim.start()


