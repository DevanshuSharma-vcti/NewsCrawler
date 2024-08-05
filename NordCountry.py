import os
import platform
import subprocess
import time
import requests
from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection

def connect_nord_vpn(country):
    version = platform.system()
    # old_ip = check_old_ip()
    print(version)
    print('VPN Country : {}'.format(country))
    os.chdir("/usr/bin")
    global server # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    server = "nordvpn -c -g \'" + country + "\'" + ""
    p = subprocess.Popen(server, shell=True)
    p.wait()
    time.sleep(10)
    # check_ip_changed(old_ip)
    # server = "nordvpn -c -g \'"+country+"\'"+" > /dev/null 2>&1"
    # os.system(server)
    response = requests.get("https://ipinfo.io/json")
    print(response.json()['country'])
    print(response.json()["region"])
    print(response.json()["ip"])





connect_nord_vpn("United States")
# terminate_VPN()
# p = subprocess.Pclose(server, shell=True)
