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

# Install dependencies
echo "----- Install dependencies -----"

sudo chmod +x dependencies.sh
sudo ./dependencies.sh

echo "----- Dependencies installed -----"

# Create .env file
echo "----- Create .env file -----"

sudo chmod +x env_file_creator.sh
sudo ./env_file_creator.sh

echo "----- Created .env file -----"

# Launch docker-compose
echo "----- Run docker-compose -----"

sudo docker-compose build
sudo docker-compose up -d

echo "----- Finish -----"