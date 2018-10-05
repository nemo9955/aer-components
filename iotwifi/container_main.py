#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os
import json

from fabric.api import run, quiet
from fabric.contrib.files import  append
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "8080"

DOCKER_BASE_IMAGE = {
    "armv7l": "sdelrio/rpi-hostap"
}


# def populate_conf(alconf):
#     ctype = CONT_NAME.upper().replace("-", "_")
#     alconf[ctype + "_CONT_NAME"] = CONT_NAME
#     alconf[ctype + "_IMG_NAME"] = DOCKER_BASE_IMAGE[util.dev_type()]

def get_config(alconf):
    the_config = {
        "dnsmasq_cfg": {
            "address": "/#/192.168.42.1",
            "dhcp_range": "192.168.42.50,192.168.42.150,24h",
            "vendor_class": "set:device,IoT"
        },
        "host_apd_cfg": {
            "ip": "192.168.42.1",
            "ssid": alconf.var.AP_SSID,
            "wpa_passphrase": alconf.var.AP_PASS,
            "channel": "6"
        },
        "wpa_supplicant_cfg": {
            "cfg_file": "/etc/wpa_supplicant/wpa_supplicant.conf"
        }
    }
    return the_config


def run_container(alconf):
    # util.ensute_custom_network_bridge()
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    if run("test -e /sbin/wpa_supplicant ", quiet=True).succeeded:
        run("sudo systemctl mask wpa_supplicant.service")
        run("sudo mv /sbin/wpa_supplicant /sbin/no_wpa_supplicant")
        run("sudo pkill wpa_supplicant")

    # print(json.dumps(get_config(alconf), indent=2))
    # print(json.dumps(alconf, indent=2))
    # with quiet():
    run("rm -f ~/wificfg.json")
    append("~/wificfg.json", json.dumps(get_config(alconf), indent=2) )

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)

    run(' docker run ' +
        ' --restart unless-stopped ' +
        ' -dt ' +
        ' --privileged ' +
        ' --network host ' +
        ' -v ~/wificfg.json:/cfg/wificfg.json  ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name)

    util.print_cont_status(CONT_NAME)
