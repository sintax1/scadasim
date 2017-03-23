#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject as gobject

class DBusService(threading.Thread):

    def run(self):
        db = DBusWorker()
        db.loop.run()

 
class DBusWorker(dbus.service.Object):

    def __init__(self):
        self.session_bus = dbus.ServiceBus()
        self.name = dbus.service.BusName("com.root9b.scadasim", bus=self.session_bus)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.loop = gobject.MainLoop()
        dbusobject = SomeObject()

        dbus.service.Object.__init__(self, name, '/')

    @dbus.service.method("com.root9b.scadasim", in_signature='s', out_signature='as')
    def HelloWorld(self, hello_message):
        return ["Hello", "from example-service.py", "with unique name", self.session_bus.get_unique_name()]

    @dbus.service.method("com.root9b.scadasim", in_signature='', out_signature='')
    def Exit(self):
        self.loop.quit()


if __name__ == '__main__':
    db = DBusService()
    db.start()
