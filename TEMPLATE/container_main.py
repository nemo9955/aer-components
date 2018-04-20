#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = ""

DOCKER_BASE_IMAGE = {
    "armv7l": "template",
    "x86_64": "template"
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
    # util.create_storage_container(CONT_NAME)

    run(' docker run ' +
        ' --restart always ' +
        ' -dt ' +
        # ' --network host ' +
        ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        # ' --expose {0} '.format(CONT_PORT) +
        # ' -v $CURRENT_PATH/../{0}:/{0}:ro '.format(CONT_NAME) +
        # ' -e OH_PORT_TO_PATH="000:template" ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name)

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)
