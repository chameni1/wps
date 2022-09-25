import sys
import os
import argparse
import json
import importlib
import socket
import requests 
import re 
import whois
import time 
import nmap
import cmsdb.basic as basic
import cmsdb.core as core
import cmsdb.createindex as createindex
import ssl
from pywebio import start_server
ssl._create_default_https_context = ssl._create_unverified_context
print (" Input    Description")
print ("=======  ==============================")
print ("  [1]    CMS detection and Deep scan")
print ("  [2]    General scan")
print ("  [3]    Nmap port scan")
print ("  [0]    Exit  ")

selone = input("Enter Your Desired Option: ").lower()


if selone == "1":
    # There goes the cms detection 
    basic.clearscreen()
    basic.banner("CMS Detection And Deep Scan")
    site = basic.targetinp("") # Get The User input
    cua = basic.randomua()
    core.main_proc(site,cua)
    basic.handle_quit()

elif selone == '2':
    basic.clearscreen()
    basic.banner("General scan")
    site = basic.targetinp("") # Get The User input
    cua = basic.randomua() 
    print(" [~] Doing Whois Lookup.......{}")
    try:
            info = whois.whois(site)
            print('\033[1;32m[+] Domain Name = ',info.domain_name)
            print('[+] Registrar = ',info.registrar)
            print('[+] Whois Server = ',info.whois_server)
            print('[+] Referral Url = ',info.referral_url)
            print('[+] Creation Date = ',info.creation_date)
            print('[+] Expiration Date = ',info.expiration_date)
            print('[+] Name Servers = ',info.name_servers)
            print('[+] Emails = ',info.emails[1])
            print('[+] DNSSEC = ',info.dnssec)
            print('[+] Name = ',info.name)
            print('[+] Organization = ',info.org)
            print('[+] Address = ',info.address)
            print('[+] City = ',info.city)
            print('[+] State = ',info.state)
            print('[+] Zipcode = ',info.zipcode)
            print('[+] Country = \033[1;m',info.country)
    except Exception:
            print(' Some Error occurred while getting whois information..')
    basic.handle_quit()        
elif selone == "3":
    basic.clearscreen()
    basic.banner("Nmap port scan")
    site = basic.targetinp("") # Get The User input
    cua = basic.randomua()  
    try:
         if site.startswith('http://'):
                site = site.replace('http://','')
         elif site.startswith('https://'):
             site = site.replace('https://','')
    except: 
        pass
    site = site.replace('/',"")
    print("target : ",site)                     
    ip = socket.gethostbyname(site)
    print ("Adresse IP :",ip)
    nmScan = nmap.PortScanner()
    nmScan.scan(ip, '21-443')
    for host in nmScan.all_hosts():
        print('Host:%s (%s)' %(host,nmScan[host].hostname()))
        print('State:%s' %nmScan[host].state())
        for proto in nmScan[host].all_protocols():
            print('---------')
            print('Protocol: %s' %proto)
            lport=nmScan[host][proto].keys()
            for port in lport:
                print ('port : %s\tstate : %s' %(port, nmScan[host][proto][port]['state']))
    basic.handle_quit()

elif selone =='0':
       
    basic.bye()   
else:
    basic.error("Invalid Input!")
    
