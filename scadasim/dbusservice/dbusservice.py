#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject as gobject
import threading
import time
from datetime import datetime

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class DBusService(threading.Thread):

    def __init__(self):
        super(DBusService, self).__init__()
        self._stop = threading.Event()
        self.sensors = None
        self.plcs = None
        self.read_frequency = 1
        self.speed = 1
        self.active = True

    def run(self):
        log.debug('Starting read sensors worker thread')
        self._read_sensors()

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.db = DBusWorker(self.plcs)
        log.debug('Starting dbus main thread')
        self.db.loop.run()

    def set_speed(self, speed):
        self.speed = speed

    def load_plcs(self, plcs):
        self.plcs = plcs

    def _read_sensors(self):

        if self._stop.is_set(): return

        log.debug("%s Reading Sensors %s" % (self, datetime.now()))

        for plc in self.plcs:
            for sensor in self.plcs[plc]['sensors']:
                read_sensor = self.plcs[plc]['sensors'][sensor]['read_sensor']
                self.plcs[plc]['sensors'][sensor]['value'] = read_sensor()

        # Calculate the next run time based on simulation speed and read frequency
        delay = (-time.time()%(self.speed*self.read_frequency))
        t = threading.Timer(delay, self._read_sensors)
        t.daemon = True
        t.start()

    def activate(self):
        self._stop.clear()
        self.start()

    def deactivate(self):
        self._stop.set()
        self.db.loop.quit()

 
class DBusWorker(dbus.service.Object):

    def __init__(self, plcs):
        self.session_bus = dbus.SystemBus()
        self.name = dbus.service.BusName("com.root9b.scadasim", bus=self.session_bus)
        self.loop = gobject.MainLoop()
        self.plcs = plcs
        
        dbus.service.Object.__init__(self, self.name, '/')

    """
    Coil/Register Numbers   Data Addresses  Type        Table Name                          Use
    1-9999                  0000 to 270E    Read-Write  Discrete Output Coils               on/off read/write
    10001-19999             0000 to 270E    Read-Only   Discrete Input Contacts             on/off readonly
    30001-39999             0000 to 270E    Read-Only   Analog Input Registers              analog readonly
    40001-49999             0000 to 270E    Read-Write  Analog Output Holding Registers     analog read/write

    Each coil or contact is 1 bit and assigned a data address between 0000 and 270E.
    Each register is 1 word = 16 bits = 2 bytes

    dbus-send --system --type=method_call --print-reply --dest=com.root9b.scadasim / org.freedesktop.DBus.Introspectable.Introspect

    """

    #https://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#basic-type-conversions
    @dbus.service.method("com.root9b.scadasim", in_signature='s', out_signature='a{sq}')
    def registerPLC(self, plc):
        """
            return sensor name and sensor address in PLC.
            TODO: add slave id

        dbus-send --system --print-reply --dest=com.root9b.scadasim / com.root9b.scadasim.registerPLC string:"hello"
        """
        self.plcs[plc].registered = True
        log.debug("%s sensors:" % plc)
        log.debug("%s" % self.plcs[plc]['sensors'])
        return self.plcs[plc]['sensors']

    @dbus.service.method("com.root9b.scadasim", in_signature='s', out_signature='a{sq}')
    def readSensors(self, plc):
        return self.plcs[plc]['sensors']

    @dbus.service.method("com.root9b.scadasim", in_signature='', out_signature='a{sv}')
    def dictTest(self, plc):
        return self.plcs[plc]['sensors']


if __name__ == '__main__':
    db = DBusService()
    db.start()
