#!/bin/bash
echo "Stop container"
docker compose down
echo "Start container"
docker compose up -d
echo "Finish deploying!"
