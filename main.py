import upnpy


def select_gateway():
    upnp = upnpy.UPnP()
    devices = upnp.discover()
    device = upnp.get_igd()
    """if len(devices) == 0:
        raise RuntimeError("No gateway was found. Try again.")
    i = 0
    for d in devices:
        print(i, "- ", d)
        i += 1
    index = int(input("Please select your gateway, enter a number: "))
    while index < 0 or index >= len(devices):
        index = int(input("Error. Please select a valid number corresponding to your gateway: "))
    device = devices[index]
    """
    return device


def main(device):
    service_name = list(device.services.keys())[0]
    service = device[service_name]

    print(service.get_actions())

    # Finally, get the external IP address
    # Execute the action by its name
    # Returns a dictionary: {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
    print(service.GetExternalIPAddress())

    #print(service.AddPortMapping.get_input_arguments())
    #print(service.DeletePortMapping.get_input_arguments())
    #print("here ", service.GetSpecificPortMappingEntry(NewRemoteHost='', NewExternalPort=21181, NewProtocol='TCP'))
    
    """service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=21180,
        NewProtocol='TCP',
        NewInternalPort=22000,
        NewInternalClient='192.168.1.149',
        NewEnabled=1,
        NewPortMappingDescription='Test port mapping entry from UPnPy.',
        NewLeaseDuration=0
    )"""
    #print("whatch this: ", service.GetGenericPortMappingEntry(NewPortMappingIndex=0))
    
    """service.DeletePortMapping(
        NewRemoteHost='',
        NewExternalPort=21180,
        NewProtocol='TCP')
       """ 
def add_port_mapping( service,external_port, protocol, internal_port, client_ip, description='', lease_duration=0):
    try:
        service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=external_port,
        NewProtocol=protocol,
        NewInternalPort=internal_port,
        NewInternalClient=client_ip,
        NewEnabled=1,
        NewPortMappingDescription=description,
        NewLeaseDuration=lease_duration
        )

    except Exception:
        print("Error while adding the portmapping.")
        
main(select_gateway())