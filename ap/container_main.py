#!/usr/bin/env python3
# pylint: disable=I0011,E1129,E0602

import os
import sys
from os.path import join as pjoin

from fabric.api import run, cd, quiet, sudo
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)

# DOCKER_BASE_IMAGE = {
#     "armv7l": "ap"
# }

"""
interface=wlan0
interface=__AP_INTERFACE__
ssid=__AP_SSID__
channel=__AP_CANNEL__
wpa_passphrase=__AP_WPA_PASSPHRASE__

address __AP_ADDRRESS_ROUTE__
192.168.42.1
netmask __AP_ADDRRESS_NETMASK__
255.255.255.0
network __AP_ADDRRESS_NETWORK__
192.168.42.0
broadcast __AP_ADDRRESS_BROADCAST__
192.168.42.255

 __AP_DNSMASK_ADDRRESS_START__
192.168.42.50
 __AP_DNSMASK_ADDRRESS_STOP__
192.168.42.150
 __AP_DNSMASK_LEASETIME__
 12h
"""


# def populate_conf(alconf):
#     ctype = CONT_NAME.upper().replace("-", "_")
#     alconf[ctype + "_CONT_NAME"] = CONT_NAME
#     alconf[ctype + "_IMG_NAME"] = DOCKER_BASE_IMAGE[util.dev_type()]
#     alconf[ctype + "_SSID"] = AP_SSID
#     alconf[ctype + "_PASS"] = AP_PASS


def replace_here(alconf):
    replace_list = [
        ("__AP_INTERFACE__", "wlan0"),
        ("__AP_SSID__", alconf.var.AP_SSID),
        ("__AP_WPA_PASSPHRASE__", alconf.var.AP_PASS),
        ("__AP_CANNEL__", "4"),
        ("__AP_ADDRRESS_ROUTE__", "192.168.42.1"),
        ("__AP_ADDRRESS_NETMASK__", "255.255.255.0"),
        ("__AP_ADDRRESS_NETWORK__", "192.168.42.0"),
        ("__AP_ADDRRESS_BROADCAST__", "192.168.42.255"),
        ("__AP_DNSMASK_ADDRRESS_START__", "192.168.42.50"),
        ("__AP_DNSMASK_ADDRRESS_STOP__", "192.168.42.150"),
        ("__AP_DNSMASK_LEASETIME__", "12h")
    ]

    print(cyan("Replacing tags with proper values : "),)
    for org_, chg_ in replace_list:
        print(cyan(". "),)
        sys.stdout.flush()
        run(" find ./ -type f -exec sed -i -e 's/%s/%s/g' {} \; " % (org_, chg_))
    print(" ")
    sys.stdout.flush()


def run_container(alconf):
    if util.dev_type() != "armv7l":
        print(red("this is not an ARM dev board ... armv7l "))
        return False

    util.to_host(pjoin(CONT_PATH, "apc"))

    with cd("apc"), quiet():
        replace_here(alconf)

    # return
#     sudo("cp -f apc/etc/sysctl.conf /etc/sysctl.conf ")
#     # sudo("cp -f apc/etc/rc.local /etc/rc.local ")
#     sudo("cp -f apc/etc/iptables.test.rules /etc/iptables.test.rules ")
#     sudo("cp -f apc/etc/network/if-pre-up.d/iptables /etc/network/if-pre-up.d/iptables ")

    # sudo("apt-get update -y")
    # sudo("apt-get dist-upgrade -y")

    sudo("apt-get install -y dnsmasq hostapd dhcpcd5 ")

    sudo("systemctl enable dhcpcd")
    sudo("systemctl stop hostapd")
    sudo("systemctl stop dhcpcd")
    sudo("systemctl stop dnsmasq")

    sudo("cp -f apc/etc/dhcpcd.conf /etc/dhcpcd.conf ")
    sudo("cp -f apc/etc/network/interfaces /etc/network/interfaces ")

    sudo("service dhcpcd restart")
    sudo("ifdown wlan0")
    sudo("ifup wlan0")

    sudo("cp -f apc/etc/dnsmasq.conf /etc/dnsmasq.conf ")
    sudo("cp -f apc/etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf ")
    sudo("cp -f apc/etc/default/hostapd /etc/default/hostapd ")

    sudo("service dhcpcd  start")
    sudo("service dnsmasq start")
    sudo("service hostapd start")
    sudo("service wpa_supplicant stop")
    sudo("systemctl disable wpa_supplicant")
