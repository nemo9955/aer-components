#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "8123"


DOCKER_BASE_IMAGE = {
    "armv7l": "lroguet/rpi-home-assistant",
    "x86_64": "homeassistant/home-assistant"
}


def run_container(alconf):
    util.ensute_custom_network_bridge()
    util.ensure_cont_stopped(CONT_NAME)

    run("mkdir -p $HOME/%s" % CONT_NAME)
    run("rm $HOME/%s/configuration.yaml" % CONT_NAME)

    util.to_host(os.path.join(CONT_PATH, "configuration.yaml"))
    run("cp configuration.yaml $HOME/%s/" % CONT_NAME)

    run(" docker run " +
        " -dt " +
        '--network host ' +
        # " --network {} ".format(alconf.var.docker_network_name) +
        # '--ip "192.168.59.123"  ' +
        ' --expose {} '.format(CONT_PORT) +
        # ' -p {0}:{0} '.format(CONT_PORT) +
        # ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        " --restart always " +
        " --name %s " % CONT_NAME +
        " --log-opt max-size=250k --log-opt max-file=4  " +
        " " +
        " -v /etc/localtime:/etc/localtime:ro " +
        " -v $HOME/%s:/config " % CONT_NAME +
        # ' -e OH_PORT_TO_PATH="8123: hass, 8123: homeassistant" ' +
        " " + DOCKER_BASE_IMAGE[util.dev_type()])

    util.print_cont_status(CONT_NAME)


# def generate_meta(util.dev_type()):
# run("echo \"#!/usr/bin/env bash\" > meta-source.sh")

#     files.append("meta-source.sh", "CONTAINER_NAME=" + CONT_NAME)
#     files.append("meta-source.sh", "IMAGE_NAME=" +
#                  DOCKER_BASE_IMAGE[util.dev_type()])
