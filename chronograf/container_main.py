#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "8888"

DOCKER_BASE_IMAGE = {
    "armv7l": "chronograf",
    "x86_64": "chronograf"
}

#  https://hub.docker.com/_/chronograf/

def run_container(alconf):
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    # excluded = [".git", "lib", ".gitignore", "README.md", ".vscode"]
    # util.to_host(os.path.join(CONT_PATH, "DATA"),rename="data", exclude=excluded)

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)

    run(' docker run ' +
        ' --restart always ' +
        ' -dt ' +
        ' --net=net_database '+
        # ' --network host ' +
        # '--link influxdb ' +
        # '--link kapacitor ' +
        # ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        ' -p {0}:{0} '.format(CONT_PORT) +
        # ' --expose $CONT_PORT ' +
        '-v {0}-storage:/var/lib/{0} '.format(CONT_NAME) +
        # ' -v $CURRENT_PATH/../{0}:/{0}:ro '.format(CONT_NAME) +
        # ' -e OH_PORT_TO_PATH="000:template" ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name +
        ' --host 0.0.0.0 --port {} '.format(CONT_PORT) +
        # ' --basepath /chronograf --prefix-routes ' +
        ' --influxdb-url=http://influxdb:8086 ' +
        ' --kapacitor-url=http://kapacitor:9092 ')

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)
