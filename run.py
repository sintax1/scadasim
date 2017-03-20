#!/usr/bin/env python

import argparse
import threading
from scadasim.utils import parse_yml, build_simulation

parser = argparse.ArgumentParser(description='Build and run SCADA simulated environments')
parser.add_argument('-c', '--config', help='YAML configuration file to load', required=True)
args = parser.parse_args()

def run():
    config = parse_yml(args.config)
    devices = build_simulation(config)

t = threading.Thread(target=run)
t.daemon = False
t.start()
