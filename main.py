import upnpy


def select_gateway():
    try:
        upnp = upnpy.UPnP()
        devices = upnp.discover()
        device = upnp.get_igd()
        return device

    except Exception as err:
        print("Erro while discovering the gateway.")
        print(err)


def main():
    try:
        device = select_gateway()
        service_name = list(device.services.keys())[0]
        service = device[service_name]

        print(service.get_actions())

        # Finally, get the external IP address
        # Execute the action by its name
        # Returns a dictionary: {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
        print(get_external_ip(service))

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
    except Exception as err:
        print(err)

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

    except Exception as err:
        print("Error while adding the portmapping.")
        print(err)
        

def get_external_ip(service):
    try:

        ip_string = service.GetExternalIPAddress()['NewExternalIPAddress']
        return ip_string
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()