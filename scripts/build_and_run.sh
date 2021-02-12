#!/bin/bash

cd ..

docker build -t apt .
docker run -d --name=apt -it apt
