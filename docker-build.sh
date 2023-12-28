#!/bin/bash

# stop on error
set -e
source docker-name.sh

docker build -f Dockerfile -t "$image_name" .
