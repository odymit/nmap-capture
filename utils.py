import socket
import netifaces
# get localhost 
def get_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_netmask(ip):
    netmask = "255.255.255.255"
    for eachnc in netifaces.interfaces():
        infos = netifaces.ifaddresses(eachnc)
        if 2 in infos and infos[2][0]['addr'] == ip:
            netmask = infos[2][0]['netmask']

    return netmask
