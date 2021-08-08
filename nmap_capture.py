#!/usr/bin/env python
# coding=utf-8
# get local area network boundary
import os 
import re
from netaddr import IPNetwork
import threading
import subprocess
import datetime
from utils import get_ip_local, get_netmask

ip = get_ip_local()
# open tcpdump to capute flows
netmask = get_netmask(ip)
network = IPNetwork(str(IPNetwork(str(ip)+str('/')+str(netmask)).network)+'/'+str(netmask))
def start_capture(cmd):
    time = datetime.datetime.now()
    capture_cmd = "tcpdump -i wlp82s0 -vnn net {ip} -w ./capture/{name}.pcap".format(
        ip=str(network), name=time.strftime("%Y-%m-%d_%H:%M:%S")+'_nmap_flow_'+str(cmd))
    tcpdump = subprocess.Popen(capture_cmd, shell=True)
    os.popen("ps -ef | grep nmap > ./capture/{name}.txt".format(name=time.strftime("%Y-%m-%d_%H:%M:%S")+'_nmap_port'))
    return tcpdump
dump = start_capture("sP")
# get alive ip list
print("scanning lan alive host, this may take a few minutes...")
cmd_out = os.popen("nmap -sP "+ str(ip) + ' ' + str(netmask))
content = cmd_out.read()
p = "Nmap scan report for ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\nHost is up"
alive_ips = re.findall(p, content)
dump.terminate()
'''sS, sT, sF, sX, sN, sV, sU, sO, sA'''
cmd_list = [
    "nmap -sA ",
    "nmap -sS ",
    "nmap -sT ",
    "nmap -sF ",
    "nmap -sX ",
    "nmap -sN ",
    "nmap -sV ",
    "nmap -sO ",
    "nmap -sU ",
]
for each_ip in alive_ips:
    for nmap_cmd in cmd_list:
        dump = start_capture(nmap_cmd[-3:-1])
        cmd = nmap_cmd + str(each_ip) + ' ' + str(netmask)
        print(cmd)
        os.system(cmd)
        dump.terminate()
