#!/bin/bash
docker build -t amazon_price_tracker .
docker run -d --name=amazon_price_tracker -it amazon_price_tracker
