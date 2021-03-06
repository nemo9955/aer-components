#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
CONT_PORT = "9995"
CONT_PORT_VIZ = "9996"

DOCKER_BASE_IMAGE = "respir-mesh-server"

def run_container(alconf):
    util.ensute_custom_network_bridge("net_database")
    # util.ensute_custom_network_bridge()
    # import json
    # print(json.dumps(alconf,indent=2))

    REM_SERVER_PATH = "$HOME/RespirMeshServer"
    if run("hostname").strip() == alconf.var.DEV_HOSTNAME:
        print(yellow("Quick referencing the local dev files of the server"))
        REM_SERVER_PATH = os.path.join(alconf.root, "RespirMesh")
    else:
        print(yellow("Copying most of the server files to the host"))
        excluded = [".git", "lib", ".gitignore", "README.md", ".vscode"]
        run("rm -rf $HOME/RespirMeshServer ")
        util.to_host(os.path.join(alconf.pth.root, "RespirMesh"),
                     rename="RespirMeshServer", exclude=excluded)
        run(" cp -r RespirMeshServer $HOME ")

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, DOCKER_BASE_IMAGE)
    # util.create_storage_container(CONT_NAME)

    run(' docker run ' +
        ' --restart always ' +
        ' --net=net_database '+
        ' -dt ' +
        ' -p {0}:{0} '.format(CONT_PORT) +
        ' -p {0}:{0} '.format(CONT_PORT_VIZ) +
        # ' --network host ' +
        # ' -p 127.0.0.1:{0}:{0} '.format(CONT_PORT) +
        ' -v %s:/RespirMeshServer ' % REM_SERVER_PATH +
        # ' --expose {0} '.format(CONT_PORT) +
        # ' --expose 9996 ' +
        # ' -v $CURRENT_PATH/../{0}:/{0}:ro '.format(CONT_NAME) +
        # ' -e OH_PORT_TO_PATH="000:template" ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        DOCKER_BASE_IMAGE)

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)
