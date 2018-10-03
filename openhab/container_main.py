#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

# from __init__ import utils, util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)

DOCKER_BASE_IMAGE = {
    "armv7l": "openhab/openhab:2.3.0-armhf-debian",
    "x86_64": "openhab/openhab:2.3.0-arm64-debian"
}


# # def populate_conf(alconf):
# #     ctype = CONT_NAME.upper().replace("-", "_")
# #     alconf[ctype + "_CONT_NAME"] = CONT_NAME
# #     alconf[ctype + "_IMG_NAME"] = DOCKER_BASE_IMAGE[util.dev_type()]
# #     alconf.OPENHAB_PORT = "8080"
#     # alconf.OPENHAB_CONT_NAME = CONT_NAME
#     # alconf.OPENHAB_IMG_NAME = DOCKER_BASE_IMAGE[util.dev_type()]


# def run_container(alconf):
#     df_name = "Dockerfile-" + util.dev_type()

#     # excluded = [".git", "lib", ".gitignore", "README.md", ".vscode"]
#     # util.to_host(os.path.join(CONT_PATH, "DATA"),
#     #               rename="data", exclude=excluded)
#     # util.to_host(os.path.join(CONT_PATH, df_name), rename="Dockerfile")
#     util.to_host(os.path.join(CONT_PATH, "run-container.sh"))

#     print(cyan("Executting ./run-container.sh"))
#     run("chmod +x ./run-container.sh")
#     run("/bin/sh -c ./run-container.sh")

#     util.is_running(CONT_NAME)


def run_container(alconf):
    util.ensute_custom_network_bridge("net_database")
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    util.create_storage_container(CONT_NAME)

    run("mkdir -p $HOME/" + CONT_NAME)

    run(' docker run ' +
        ' --restart always ' +
        ' -td ' +
        # ' --network=host ' +
        ' --net=net_database '+

        ' -v /etc/localtime:/etc/localtime:ro ' +
        ' -v /etc/timezone:/etc/timezone:ro ' +

        # ' -e OPENHAB_HTTP_PORT="7123" ' +
        ' -p 7123:8080 ' +

        ' -v $HOME/openhab/addons:/openhab/addons ' +
        ' -v $HOME/openhab/conf:/openhab/conf ' +
        ' -v $HOME/openhab/userdata:/openhab/userdata ' +

        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name)

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)
