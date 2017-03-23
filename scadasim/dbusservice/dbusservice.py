#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject as gobject
import threading

class DBusService(threading.Thread):

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        db = DBusWorker()
        db.loop.run()

 
class DBusWorker(dbus.service.Object):

    def __init__(self):
        self.session_bus = dbus.SystemBus()
        self.name = dbus.service.BusName("com.root9b.scadasim", bus=self.session_bus)
        self.loop = gobject.MainLoop()

        dbus.service.Object.__init__(self, self.name, '/')

    """
    Coil/Register Numbers   Data Addresses  Type        Table Name
    1-9999                  0000 to 270E    Read-Write  Discrete Output Coils
    10001-19999             0000 to 270E    Read-Only   Discrete Input Contacts
    30001-39999             0000 to 270E    Read-Only   Analog Input Registers
    40001-49999             0000 to 270E    Read-Write  Analog Output Holding Registers

    Each coil or contact is 1 bit and assigned a data address between 0000 and 270E.
    Each register is 1 word = 16 bits = 2 bytes

    """

    #https://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#basic-type-conversions
    @dbus.service.method("com.root9b.scadasim", in_signature='s', out_signature='as')
    def registerPLC(self, hostname):
        """
            return sensor name and sensor address in PLC.
                TODO: add slave id
        """
        return {'Sensor1': 0x1001, 'Sensor2': 0x2001}

    @dbus.service.method("com.root9b.scadasim", in_signature='', out_signature='')
    def readSensors(self, hostname):
        return {'Sensor1': 0x00, 'Sensor2': 0xff}


if __name__ == '__main__':
    db = DBusService()
    db.start()
