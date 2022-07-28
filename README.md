# UPNPy client

This script uses the UPnP protocol to add and delete port forwarding rules to your Internet Gateway Device. This is potentially helpful if you want to connect two devices that reside behind NAT. Note that this program works with UPnP 1.0 and does not contain functions that are featured in UPnP 2.0.


## Requirements

You need to install the following libraries:  
- UPNPy
- netifaces

## How to use

Run the script as follows:  
`python main.py -a EXTERNAL_PORT INTERNAL_PORT PROTOCOL`  
This adds a rule to your IGD, provided that EXTERNAL_PORT is not taken by another rule.

`python main.py -d EXTERNAL_PORT PROTOCOL`  
The above command will delete the specified port forwarding rule.

`python -q extip`  
You  may use this to obtain your external IP address.
