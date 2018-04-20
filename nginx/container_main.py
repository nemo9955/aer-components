#!/usr/bin/env python3
# pylint: disable=I0011,E1129

import os

from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

from aer.commands.component import util

CONT_PATH = os.path.dirname(os.path.realpath(__file__))
CONT_NAME = os.path.basename(CONT_PATH)
# CONT_PORT = ""

DOCKER_BASE_IMAGE = {
    "armv7l": "nginx:1.13",
    "x86_64": "nginx:1.13"
}


def run_container(alconf):
    arch_img_name = DOCKER_BASE_IMAGE[util.dev_type()]

    # excluded = [".git", "lib", ".gitignore", "README.md", ".vscode"]
    # util.to_host(os.path.join(CONT_PATH, "DATA"),rename="data", exclude=excluded)

    run("rm -rf $HOME/nginx")
    run("mkdir -p $HOME/nginx/conf.d")

    util.to_host(os.path.join(CONT_PATH, "nginx.conf"),
                 rename="$HOME/nginx/nginx.conf")
    util.to_host(os.path.join(CONT_PATH, "default.conf"),
                 rename="$HOME/nginx/conf.d/default.conf")

    util.ensure_cont_stopped(CONT_NAME)
    util.build_latest_image(CONT_NAME, arch_img_name)
    # util.create_storage_container(CONT_NAME)

    run('export DOCKER_OPTS="--auth=identity --host=tcp://0.0.0.0:2376" && docker run ' +
        ' --network host ' +
        ' --restart always ' +
        # ' -e DOCKER_HOST=tcp://0.0.0.0:2376 ' +
        ' -v /var/run/docker.sock:/var/run/docker.sock:ro ' +
        ' -dt ' +
        '  ' +
        ' -p 80:80 ' +
        ' -v $HOME/nginx/conf.d:/etc/nginx/conf.d ' +
        ' -v $HOME/nginx/nginx.conf:/etc/nginx/nginx.conf ' +
        '  ' +
        ' --log-opt max-size=250k --log-opt max-file=4 ' +
        ' --name {} '.format(CONT_NAME) +
        arch_img_name
        # ' --with-http_stub_status_module '
        )

    # time.sleep(5)
    # run("docker exec ##### ")
    # run("docker restart ######### ")

    util.print_cont_status(CONT_NAME)
