#!/usr/bin/env python3
##############################################################################
#                       Sctipt  Create it by NuNix                           #
#                Crear punto de accesso                                      #
#    scapy  dot11                                                            #
from scapy.all import *
import os
import signal 
import time
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234  # The port used by the server
os.system('ifconfig wlan0 down')
os.system('macchanger -r wlan0 ')
os.system('iwconfig wlan0 mode monitor')
os.system('ifconfig wlan0 up')

# interface to use to send beacon frames, must be in monitor mode
iface = "wlan0"
# generate a random MAC address (built-in in scapy)
sender_mac = "72:58:08:01:fb:db"
# SSID (name of access point)
print("Porfavor entre en Nombre del Punto de Accesso (Wifi)")
ssid = input("")
# 802.11 frame
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)
# beacon layer
beacon = Dot11Beacon(cap='' )
# cap is empty no cypher^ example ESS+privacy 
# putting ssid in the frame
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
# stack all the layers and add a RadioTap
rsn = Dot11Elt(ID='RSNinfo',
                       info=('\x01\x00'
                             '\x00\x0f\xac\x02'
                             '\x02\x00'
                             '\x00\x0f\xac\x04'
                             '\x00\x0f\xac\x02'
                             '\x01\x00'
                             '\x00\x0f\xac\x02'
                             '\x00\x00'))
frame = RadioTap()/dot11/beacon/essid
# send the frame in layer 2 every 100 milliseconds forever
# using the `iface` interface
frame.show()
hexdump(frame)

os.system('tcpdump -i wlan0  -w test.pcap&')
time.sleep(1)
print('Comenzando Punto  de Accesso, persione  CTL + C para detener... ... ...')
time.sleep(2)
def handler(signum, frame):
        res = input(" Presione CTRL-C entre 'y' para detener u otra letra para continuar")

        if res == 'y':

                exit(1)
signal.signal(signal.SIGINT, handler)


sendp(frame, inter=0.01, iface=iface, loop=1)



