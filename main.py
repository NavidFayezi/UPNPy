import upnpy


def select_gateway():
    upnp = upnpy.UPnP()
    devices = upnp.discover()
    if len(devices) == 0:
        raise RuntimeError("No gateway was found. Try again.")
    i = 0
    for d in devices:
        print(i, "- ", d)
        i += 1
    index = int(input("Please select your gateway, enter a number: "))
    device = devices[index]
    return device


def main(device):
    a = device.services.keys()
    print(list(a))
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
    """service.DeletePortMapping(
        NewRemoteHost='',
        NewExternalPort=21180,
        NewProtocol='TCP')"""


main(select_gateway())