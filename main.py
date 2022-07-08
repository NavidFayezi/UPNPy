import upnpy
import netifaces



def get_local_ip():
    if_list = netifaces.interfaces()
    # In other machines you have to choose the right interface from "if_list".
    # On my machine that is eth0.
    ipv4_addresses = netifaces.ifaddresses('eth0')[netifaces.AF_INET]
    local_ipv4 = ipv4_addresses[0]['addr']
    # Attention! There might be more than one ipv4 address for one interface.
    # Make sure to choose the right one from "ipv4_addresses".
    return local_ipv4


def select_gateway():
    try:
        upnp = upnpy.UPnP()
        devices = upnp.discover()
        device = upnp.get_igd()
        return device

    except Exception as err:
        print("Error while discovering the gateway.")
        print(err)


def main():
    try:
        print(get_local_ip())
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
        
    except Exception as err:
        print(err)


def delete_port_mapping(service, port, protocol):
    try:
        if check_port_mapping(service, port, protocol) == 1:
            service.DeletePortMapping(
                NewRemoteHost='',
                NewExternalPort=port,
                NewProtocol=protocol)

    except Exception as err:
        print("Error while deleting a portmapping.")
        print(err) 


def add_port_mapping( service,external_port, protocol, internal_port, client_ip, description='', lease_duration=604000): 
    # Lease duration is in seconds. 0 means indefinitely, which sets it to the maximum.
    try:
        if check_port_mapping(service, external_port, protocol) == 0:
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
        else:
            print("This rule already exists.")

    except Exception as err:
        print("Error while adding the portmapping.")
        print(err)
        

def get_external_ip(service):
    try:

        ip_string = service.GetExternalIPAddress()['NewExternalIPAddress']
        return ip_string

    except Exception as err:
        print(err)


def check_port_mapping(service, port, protocol):
    try:
        portmapping = service.GetSpecificPortMappingEntry(NewRemoteHost='', NewExternalPort=port, NewProtocol=protocol)
        return 1

    except Exception as err:
        print(err)
        return 0


if __name__ == "__main__":
    main()