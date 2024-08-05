import os
import platform
import subprocess
import time
import requests
from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection

def disconnect_nord_vpn():
    server = "nordvpn -d"
    p = subprocess.Popen(server, shell=True)
    p.wait()
    response = requests.get("https://ipinfo.io/json")
    print(response.json()['country'])
    print(response.json()["region"])
    print(response.json()["ip"])

disconnect_nord_vpn()
