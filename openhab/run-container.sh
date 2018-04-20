#!/usr/bin/env bash

# CURRENT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# source $CURRENT_PATH/../meta-source.sh

# if [[ -e $CURRENT_PATH/Dockerfile ]]; then
# 	echo "Building image for $CURRENT_PATH/Dockerfile "
# 	cd $CURRENT_PATH
# 	docker build -f $CURRENT_PATH/Dockerfile -t $OPENHAB_IMG_NAME .
# fi

# if [[ -n $(docker ps -a --format='{{.Names}}' | grep $OPENHAB_CONT_NAME) ]] ; then
# 	echo "Stopping old $OPENHAB_CONT_NAME container"
# 	docker stop $OPENHAB_CONT_NAME
# 	echo "Removing old $OPENHAB_CONT_NAME container"
# 	docker rm -f $OPENHAB_CONT_NAME
# fi


# if [[ -n "$(docker volume inspect $OPENHAB_CONT_NAME-storage 2>&1 | grep -w Error)" ]] ; then
# 	echo "Creating storage volume: $OPENHAB_CONT_NAME-storage"
# 	docker volume create --name $OPENHAB_CONT_NAME-storage
# fi

# echo "Running container of $CURRENT_PATH"




# if [[ ! -e  $HOME/$OPENHAB_CONT_NAME  ]]; then
#     mkdir $HOME/$OPENHAB_CONT_NAME
# fi

# if [[ -e  $HOME/openhab && -e $HOME/openhab/configuration.yaml ]]; then
#     rm $HOME/openhab/configuration.yaml
# fi

# if [[ -e  $CURRENT_PATH/configuration.yaml  ]]; then
#     cp $CURRENT_PATH/configuration.yaml $HOME/openhab/
# fi




# --expose $OPENHAB_PORT \
# -p 8080:8080 \
# -p 5555:5555 \
# -p 8443:8443 \
# -e OH_PORT_TO_PATH="8080:oh80,55555:oh55,8443:oh84" \
# -e OH_PORT_TO_PATH="8080:openhab" \
# docker run \
# --restart always \
# -td \
# --network=host \
# \
# -v /etc/localtime:/etc/localtime:ro \
# -v /etc/timezone:/etc/timezone:ro \
# \
# -v $HOME/openhab/addons:/openhab/addons \
# -v $HOME/openhab/conf:/openhab/conf \
# -v $HOME/openhab/userdata:/openhab/userdata \
# \
# --log-opt max-size=250k --log-opt max-file=4  \
# --name $OPENHAB_CONT_NAME \
# $OPENHAB_IMG_NAME

# -v $HOME/$OPENHAB_CONT_NAME:/openhab \


# -p $HOME_SERVER_PORT:$HOME_SERVER_PORT \
# -v $CURRENT_PATH/../$OPENHAB_CONT_NAME:/$OPENHAB_CONT_NAME:ro \