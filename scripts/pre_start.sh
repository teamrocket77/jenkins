#! /usr/bin/env bash

source volume.sh

docker network create jenkins
docker volume create $VOLUME_NAME
