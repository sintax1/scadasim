import dbus
import dbus.service
import dbus.mainloop.glib
import threading
from gi.repository import GObject as gobject

gobject.threads_init()



class DBUSService(threading.Thread):

	def __init__(self):
		super(DBUSService, self).__init__()
		self._stop = threading.Event()
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.loop = gobject.MainLoop()
		self.dbusmonitor = DBUSMonitor()
    		self.loop.run()

	def stop(self):
		self.loop.quit()
		self._stop.set()
		self.join()


class DBUSMonitor(dbus.service.Object):
    def __init__(self, iface="com.root9b.scadaplc", path="/scadasim", **kwargs):
        self.iface = iface
        self.path = path
        self.bus = dbus.SystemBus()
        self.busname = dbus.service.BusName(self.iface, self.bus)
        super(DBUSMonitor, self).__init__(self.busname, self.path, **kwargs)


    def add_signal_handler(self, signal, handler):
        self.bus.add_signal_receiver(handler, signal_name=signal,
            interface_keyword='dbus_interface', member_keyword='member')

    def add_keepalive(self, method_to_call, timeout):
        self.timer = gobject.timeout_add(timeout, method_to_call)


if __name__ == '__main__':
	db = DBUSService()
	db.start()
