#!/usr/bin/env python3
# pylint: disable=I0011,E1129


import json
import os
import time
from os.path import join as pjoin

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "3000"
DOCKER_BASE_IMAGE = {
    "armv7l": "grafana/grafana",
    "x86_64": "grafana/grafana"
}


def run_container(alconf):
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)

    run(' docker run ' +
        ' -dt ' +
        # ' --network host ' +
        '--link influxdb ' +
        # ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        # ' -p 3000:3000 ' +
        ' --expose 3000 ' +
        ' --restart always ' +
        ' --name=grafana ' +
        # ' -v $HOME/backup:/backup   ' +
        ' -v grafana-storage:/var/lib/grafana ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +

        ' -e GF_ANALYTICS_CHECK_FOR_UPDATES="false" ' +
        ' -e GF_ANALYTICS_REPORTING_ENABLED="false" ' +

        ' -e GF_SECURITY_ADMIN_USER={} '.format(alconf.var.GRAFANA_ADMIN_NAME) +
        ' -e GF_SECURITY_ADMIN_PASSWORD={} '.format(alconf.var.GRAFANA_ADMIN_PASS) +
        ' -e GF_SECURITY_USERS_ALLOW_ORG_CREATE="false" ' +
        ' -e GF_SECURITY_USERS_VERIFY_EMAIL_ENABLED="false" ' +

        ' -e GF_AUTH_ANONYMOUS_ENABLED="true" ' +
        ' -e GF_AUTH_ANNONYMUS_ORG_NAME="ORGANIZATION" ' +
        ' -e GF_AUTH_ANNONYMUS_ORG_ROLE="Viewer" ' +
        ' -e GF_AUTH_DISABLE_LOGIN_FORM="false" ' +
        ' -e GF_USERS_ALLOW_SIGN_UP="true" ' +
        ' -e GF_AUTH_PROXY="false" ' +

        ' -e GF_SERVER_ROOT_URL="%(protocol)s://%(domain)s:%(http_port)s/grafana" ' +
        # ' -e GF_SERVER_ROOT_URL="%(protocol)s://%(domain)s:%(http_port)s/grafana" ' +
        # ' -e OH_PORT_TO_PATH="3000:grafana" ' +
        # ' -e VIRTUAL_HOST="grafana.192.168.2.111"  ' +
        arch_img_name)

    # TODO Function to wait until .... maybe an API call

    # time.sleep(10)
    # run("docker exec grafana grafana-cli plugins install grafana-clock-panel")
    # run("docker exec grafana grafana-cli plugins install grafana-worldmap-panel")
    # run("docker exec grafana grafana-cli plugins install natel-influx-admin-panel")
    # run("docker exec grafana grafana-cli plugins install grafana-piechart-panel")
    # run("docker exec grafana grafana-cli plugins update-all")
    # run("docker restart grafana")

    util.print_cont_status(CONT_NAME)

    # # util.to_host(os.path.join(CONT_PATH, "run-container.sh"))

    # # generate_meta(util.dev_type())

    # print( cyan("Executting ./run-container.sh"))
    # run("chmod +x ./run-container.sh")
    # run("/bin/sh -c ./run-container.sh")

    # util.is_running(CONT_NAME)
