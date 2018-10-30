#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run, sudo
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_NAME_DNS = CONT_NAME+"_dns"


DOCKER_BASE_IMAGE = {
    "armv7l": "pihole/pihole:v4.0_armhf",
    "x86_64": "pihole/pihole:v4.0_amd64"
}


# def populate_conf(alconf):
#     ctype = CONT_NAME.upper().replace("-", "_")
#     alconf[ctype + "_CONT_NAME"] = CONT_NAME
#     alconf[ctype + "_IMG_NAME"] = DOCKER_BASE_IMAGE[util.dev_type()]


def run_container(alconf):
    # util.ensute_custom_network_bridge()
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    # excluded = [".git", "lib", ".gitignore", "README.md", ".vscode"]
    # util.to_host(os.path.join(CONT_PATH, "DATA"),rename="data", exclude=excluded)

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)
    util.create_storage_container(CONT_NAME_DNS)

    # ipv6ip = run("ip -6 route get 2001:4860:4860::8888 | awk '{for(i=1;i<=NF;i++) if ($i==\"src\") print $(i+1)}'")
    # docker ipv6 needs to be activated : https://docs.docker.com/config/daemon/ipv6/

    sudo('fuser -k -n tcp 53')
    sudo('fuser -k -n udp 53')
    sudo('fuser -k -n udp 67')

    run(' docker run ' +
        ' --restart always ' +
        ' -dt ' +
        ' -v {}-storage:/etc/pihole '.format(CONT_NAME) +
        ' -v {}-storage:/etc/dnsmasq.d '.format(CONT_NAME_DNS) +
        ' --restart=unless-stopped ' +
        ' --cap-add=NET_ADMIN ' +
        ' --net=net_database ' +
        ' -p 53:53/tcp ' +
        ' -p 53:53/udp ' +
        ' -p 67:67/udp ' +
        ' -p 80:80 ' +
        ' --dns 127.0.0.1 ' +
        # ' -p 443:443 ' +
        # ' -p 8765:8765 ' +
        # ' -e WEB_PORT="8765" ' +
        ' -e WEBPASSWORD="pihole.par" ' +
        ' -e ServerIP="$(ip route get 8.8.8.8 | awk \'{ print $NF; exit }\')" ' +
        # ' -e ServerIPv6="{}" '.format(ipv6ip) +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name)

    util.print_cont_status(CONT_NAME)
