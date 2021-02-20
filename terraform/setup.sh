#!/bin/bash

set -xeou pipefail

DOCKER_COMPOSE=/usr/local/bin/docker-compose
SRC=/home/ec2-user/src

# install and start docker
sudo yum install -y docker git \
    && service docker start

# install docker-compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o $DOCKER_COMPOSE \
    && chmod +x $DOCKER_COMPOSE

# clone repo
git clone https://github.com/max-hoffman/contrary-hackathon-21.git $SRC

cd $SRC
sudo $DOCKER_COMPOSE up -d
