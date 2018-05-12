#!/usr/bin/env python3
# pylint: disable=I0011,E1129
# -*- coding: utf-8 -*-
# coding=utf-8


import datetime
import json
import os
import time
from os.path import join as pjoin

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "8086"

DOCKER_BASE_IMAGE = {
    "armv7l": "influxdb",
    "x86_64": "influxdb"
}


def run_container(alconf):
    # util.ensute_custom_network_bridge()
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    # util.to_host(os.path.join(CONT_PATH, "influxdb.conf"))
    # run("cp influxdb.conf $HOME/")

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)

    run('docker run ' +
        '-dt  ' +
        # '--network host ' +
        # " --network {} ".format(alconf.var.docker_network_name) +
        # '--ip "192.168.59.86"  ' +
        # ' -p {0}:{0} '.format(CONT_PORT) +
        # ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        '--restart always ' +
        '--log-opt max-size=250k --log-opt max-file=4  ' +
        '' +
        # ' -e INFLUXDB_REPORTING_DISABLED=true' +
        # ' -e INFLUXDB_META_DIR=/var/lib/influxdb/metadir' +
        # ' -e INFLUXDB_DATA_QUERY_LOG_ENABLED=false' +
        # ' -e INFLUXDB_ADMIN_USER=' +
        # ' -e INFLUXDB_ADMIN_PASSWORD=' +
        '' +
        # '-v $HOME/backup:/backup ' +
        '-v /etc/localtime:/etc/localtime:ro   ' +
        '-v {}-storage:/var/lib/influxdb '.format(CONT_NAME) +
        # ' -v $HOME/influxdb.conf:/etc/influxdb/influxdb.conf:ro  ' +
        '' +
        '--name {} '.format(CONT_NAME) +
        arch_img_name )
        # "  -config /etc/influxdb/influxdb.conf ")

    util.print_cont_status(CONT_NAME)

    # TODO Function to wait until .... use :8086/ping to check state
    time.sleep(15)
    run('docker exec influxdb influx -execute "CREATE DATABASE \"hass\"" ')

    run("docker restart influxdb ")

    util.print_cont_status(CONT_NAME)
