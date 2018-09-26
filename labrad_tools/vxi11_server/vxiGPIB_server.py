"""
### BEGIN NODE INFO
[info]
name = vxigpib
version = 1
description = none
instancename = %LABRADNODE%_vxigpib

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""
import sys
import vxi11

#List of ip addresses corresponding to ICS 9065 hubs
from GPIBHubList import hubList 

from labrad.server import LabradServer, setting

sys.path.append('../')
from server_tools.hardware_interface_server import HardwareInterfaceServer


class VXIGPIBServer(HardwareInterfaceServer):
    """ Provides access to GPIB hardware through ICS 9065 GPIB-Ethernet Hub.
    The ICS 9065 has a vxi11 interface which converts commands to IEEE 488.2.
    """
    name = '%LABRADNODE%_vxigpib'

    def refresh_available_interfaces(self):
        """ fill self.interfaces with gpib devices connected to gpib-ethernet hubs """
        #Get all vxi11 devices on the sesame st network
        all_addresses = vxi11.list_devices('192.168.1.255') 
        #Get all ips of currently connected gpib-ethernet hubs
        hub_addresses = [a for a in all_addresses if a in hubList.keys()]
        #Get list of GPIB resources connected to active gpib-ethernet hubs
        gpib_addresses = []
        for address in hub_addresses:
            gpib_addresses = gpib_addresses + vxi11.list_resources(address)
        for address in gpib_addresses:
            self.interfaces[address] = vxi11.Instrument(address)

    @setting(3, data='s', returns='')
    def write(self, c, data):
        """Write a string to the vxi interface."""
        self.call_if_available('write', c, data)

    @setting(4, n_bytes='w', returns='s')
    def read(self, c, n_bytes=None):
        """Read from the vxi interface."""
        response = self.call_if_available('read', c)
        return response.strip()

    @setting(5, data='s', returns='s')
    def ask(self, c, data):
        """Make a query, writes string then returns instrument response."""
        response = self.call_if_available('ask', c, data)
        return response.strip()

    @setting(6, timeout='v', returns='v')
    def timeout(self, c, timeout=None):
	"""set interface timeout"""
        interface = self.get_interface(c)
        if timeout is not None:
            interface.timeout = timeout
        return interface.timeout

if __name__ == '__main__':
    from labrad import util
    util.runServer(VXIGPIBServer())
