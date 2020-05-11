#!/bin/bash

cd scripts

# Remove old container
sudo chmod +x delete_old_docker.sh
sudo ./delete_old_docker.sh

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

cd ..

# Remove old errors.log
if [ -f "errors.log" ]; then
  rm errors.log
fi

# Launch docker-compose
echo "----- Run docker-compose -----"

sudo docker-compose build
sudo docker-compose up -d

echo "----- Finish -----"