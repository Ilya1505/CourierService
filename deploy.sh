#!/bin/bash
echo "Pulling changes"
git pull
echo "Stop container"
docker compose down
echo "Start container"
docker compose up -d
echo "Finish deploying!"
