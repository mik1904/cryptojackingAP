# cryptojackingAP
A malicious access point that injects mining scripts on the fly.
## Requirements
- iptables
- python3

## Set-up
The tool is a PoC of a rouge access point that injects cryptomining code in the webpages
requested by the connected users using HTTP (no HTTPS support). I run a proof of concept on a raspberry Pi, you can search online how to set up an access point. In this code I give as granted that you have set up an access point on a Linux machine (in my case Ubuntu 16.04).

## Instructions
First run the bash script:
```
$ sudo iptables_maliciousAP.sh
```
Please note that you might have to change the network interface's name accordingly. 
In this example, wlan0 is the interfaces that is connecting to the internet while 
wlan1 is the interface where the access point is running and users conenct.

After running the script, request coming in at wlan1, with destination port 80 (HTTP), are forwarded 
to the localhost on port 9090. Now is time to run the python script:
``` 
$ python3 malicious_webserver.py
```
The latter, receives the requests forwarded by the iptables, retrieves the requested data, 
injects the cryptomining code (if possible) and returns everything to the client. 

