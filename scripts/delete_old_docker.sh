#!/bin/bash

# Remove old container
echo "----- Stop old container -----"
sudo docker stop $(sudo docker ps --filter name=tracker_bot --filter name=tracker_db --filter name=tracker_phpmyadmin -q)

echo "----- Remove old container -----"
sudo docker rm $(sudo docker ps -a --filter name=tracker_bot --filter name=tracker_db --filter name=tracker_phpmyadmin -q)

echo "----- Remove old volumes -----"
sudo docker volume rm $(sudo docker volume ls --filter name=amazonpricetracker_mariadb)

echo "----- Remove old network -----"
sudo docker network rm $(sudo docker network ls --filter name=amazonpricetracker_default)
