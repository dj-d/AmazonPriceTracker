#!/bin/bash

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