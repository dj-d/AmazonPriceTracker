#!/bin/bash

cd ..

docker build -t tracker_bot .
docker run -d --name=tracker_bot -it tracker_bot
