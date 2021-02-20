#!/bin/bash

set -xeou pipefail

DIR=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
BASE=$DIR

PYTHON_VERSION=3.7
ZIP_TARGET=$BASE/layer.zip
LAYER_DIR=python/lib/"python$PYTHON_VERSION"/site-packages
CONTAINER_HOME=/home

sudo rm -rf zip layer.zip && mkdir -p zip/$LAYER_DIR

PIP_OPTS="-t $CONTAINER_HOME/zip/$LAYER_DIR"

docker run \
   --rm \
   -v $BASE:$CONTAINER_HOME \
   -w $CONTAINER_HOME \
   lambci/lambda:build-python${PYTHON_VERSION} \
   /bin/bash -c "pip install $PIP_OPTS uvicorn fastapi"

cd $BASE/zip
sudo rm -r $LAYER_DIR/botocore $LAYER_DIR/numpy/tests $LAYER_DIR/pyarrow/tests $LAYER_DIR/pandas/tests
zip -ur $ZIP_TARGET $LAYER_DIR
