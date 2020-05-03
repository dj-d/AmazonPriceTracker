#!/bin/bash

CREDENTIAL_FILE="credentials.json"

# Remove old .env file
rm .env

# Create new .env file
touch .env

# Insert data into file
DB_NAME=$(jq .db.db_name $CREDENTIAL_FILE)
echo "MYSQL_DATABASE=${DB_NAME//\"}" >> .env

DB_ROOT_PASSWORD=$(jq .db.root_password $CREDENTIAL_FILE)
echo "MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD//\"}" >> .env

DB_USER=$(jq .db.user $CREDENTIAL_FILE)
echo "MYSQL_USER=${DB_USER//\"}" >> .env

DB_USER_PASSWORD=$(jq .db.user_password $CREDENTIAL_FILE)
echo "MYSQL_PASSWORD=${DB_USER_PASSWORD//\"}" >> .env

echo "MYSQL_PORT=$(jq .db.port $CREDENTIAL_FILE)" >> .env
