import dbus
import dbus.service
import dbus.mainloop.glib
import threading
from gi.repository import GObject as gobject


class DBUSService(dbus.service.Object, threading.Thread):
    def __init__(self, iface="com.root9b.scadaplc", path="/scadasim"):
        gobject.threads_init()

        dbus.mainloop.glib.threads_init()
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.iface = iface
        self.path = path

        self.bus = dbus.SystemBus()
        self.busname = dbus.service.BusName(self.iface, self.bus)
        
        dbus.service.Object.__init__(self, self.busname, self.path)
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        self.loop = gobject.MainLoop()
        self.loop.run()

    def stop(self):
        self.loop.quit()
        self._stop.set()

if __name__ == '__main__':
    db = DBUSService()
    db.daemon = True
    db.run()
