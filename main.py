import upnpy
import netifaces
import sys


HELP_MSG = "Use the script as follows:\n\
python main.py -a EXTERNAL_PORT INTERNAL_PORT PROTOCOL      *This adds a portmapping.\n\
python main.py -d EXTERNAL_PORT PROTOCOL                    *This deletes a portmapping."

# Note: It is not possible to add a portmapping for an "Internal Client" for other IPs.
# You may only add portmappings for your own IP address. 
def get_local_ipv4():
    try:
        if_list = netifaces.interfaces()
        # In other machines you have to choose the right interface from "if_list".
        # On my machine that is eth0.
        ipv4_addresses = netifaces.ifaddresses('eth0')[netifaces.AF_INET]
        local_ipv4 = ipv4_addresses[0]['addr']
        # Attention! There might be more than one ipv4 address for one interface.
        # Make sure to choose the right one from "ipv4_addresses".
        return local_ipv4

    except Exception as err:
        print("Error while obtaining the local ipv4 address")
        raise err


def select_gateway():
    try:
        upnp = upnpy.UPnP()
        devices = upnp.discover()
        device = upnp.get_igd()
        return device

    except Exception as err:
        print("Error while discovering the gateway.")
        raise err



def delete_port_mapping(service, port, protocol):
    try:
        if check_port_mapping(service, port, protocol)[0] == 1:
            service.DeletePortMapping(
                NewRemoteHost='',
                NewExternalPort=port,
                NewProtocol=protocol)

    except Exception as err:
        print("Error while deleting a portmapping.")
        raise err 


def add_port_mapping( service,external_port, protocol, internal_port, client_ip, description='', lease_duration=604000): 
    # Lease duration is in seconds. 0 means indefinitely, which sets it to the maximum.
    try:
        probe_res = check_port_mapping(service, external_port, protocol)
        if probe_res[0] == 0:
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
            if client_ip == probe_res[1]['NewInternalClient']:
                print("This rule already exists.")
            
            else:
                print("This port is taken, try another external port")

    except Exception as err:
        print("Error while adding the portmapping.")
        raise err
        

def get_external_ip(service):
    try:
        ip_string = service.GetExternalIPAddress()['NewExternalIPAddress']
        return ip_string
    except Exception as err:
        print("Error while obtaining the external ip address")
        raise err

def check_port_mapping(service, port, protocol):
    try:
        portmapping = service.GetSpecificPortMappingEntry(NewRemoteHost='', NewExternalPort=port, NewProtocol=protocol)
        return (1, portmapping)

    except Exception as err:
        type, code = err.args
        if type == 'NoSuchEntryInArray' and code == 714:
            return (0, None)
        
        else: 
            raise Exception("Unexpected Error in check_port_mapping")


def main():
    try:
        local_ipv4 = get_local_ipv4()
        device = select_gateway()
        service_name = list(device.services.keys())[0]
        service = device[service_name]

        arguments = sys.argv[:]
        operation = arguments[1]
        if operation == "-a":
            external_port = int(arguments[2])
            internal_port = int(arguments[3])
            protocol = arguments[4]
            add_port_mapping(service, external_port, protocol, internal_port, local_ipv4)
            print("Portmapping added.")

        elif operation == "-d":
            external_port = int(arguments[2])
            protocol = arguments[3]
            delete_port_mapping(service, external_port, protocol)
            print("Portmapping deleted.")

        elif operation == "-q":
            if arguments[2] == "extip":
                print("Your external IP is: ", get_external_ip(service))
            else:
                raise RuntimeError
        else: 
            raise RuntimeError

        
        #print(service.get_actions())

        # Finally, get the external IP address
        # Execute the action by its name
        # Returns a dictionary: {'NewExternalIPAddress': 'xxx.xxx.xxx.xxx'}
        
        #add_port_mapping(service, 33333, 'TCP', 22222, local_ipv4)
        #add_port_mapping(service, external_port, protocol, internal_port, local_ipv4)
        #delete_port_mapping(service, external_port, protocol)
        
    except Exception as err:
        print(err)
        print(HELP_MSG)


if __name__ == "__main__":
    main()