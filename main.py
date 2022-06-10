import upnpy


upnp = upnpy.UPnP()
devices = upnp.discover()
device = devices[0]

service = device['WANPPPConn1']

print(service.get_actions())

# Finally, get the external IP address
# Execute the action by its name
# Returns a dictionary: {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
print(service.GetExternalIPAddress())

#print(service.AddPortMapping.get_input_arguments())
print(service.DeletePortMapping.get_input_arguments())
"""service.AddPortMapping(
    NewRemoteHost='',
    NewExternalPort=21180,
    NewProtocol='TCP',
    NewInternalPort=22000,
    NewInternalClient='192.168.1.104',
    NewEnabled=1,
    NewPortMappingDescription='Test port mapping entry from UPnPy.',
    NewLeaseDuration=0
)"""
service.DeletePortMapping(
    NewRemoteHost='',
    NewExternalPort=21180,
    NewProtocol='TCP')