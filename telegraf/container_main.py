#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)

DOCKER_BASE_IMAGE = {
    "armv7l": "telegraf",
    "x86_64": "telegraf"
}

# def populate_conf(alconf):
#     ctype = CONT_NAME.upper().replace("-", "_")
#     alconf[ctype + "_CONT_NAME"] = CONT_NAME
#     alconf[ctype + "_IMG_NAME"] = DOCKER_BASE_IMAGE[util.dev_type()]


def run_container(alconf):
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    util.to_host(os.path.join(CONT_PATH, "telegraf.conf"))
    run("cp telegraf.conf $HOME/")

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)

    run(' docker run ' +
        ' --restart always ' +
        ' -dt ' +
        ' --network host ' +
        ' -v /var/run/docker.sock:/var/run/docker.sock:ro ' +
        ' -v $HOME/telegraf.conf:/etc/telegraf/telegraf.conf:ro  ' +
        # ' -p 127.0.0.1:{0}:{0} '.format() +
        # ' --expose ' +
        '-v {0}-storage:/var/lib/{0} '.format(CONT_NAME) +
        # ' -v $CURRENT_PATH/../{0}:/{0}:ro '.format(CONT_NAME) +
        # ' -e OH_PORT_TO_PATH="000:template" ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name)

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)