#!/bin/bash

# Error log file paths
MAIN_PY_ERROR_LOG="/home/pi/Desktop/Greenhouse/GreenhouseSensor/logs/main_error.log"
FLASK_SERVER_ERROR_LOG="/home/pi/Desktop/Greenhouse/GreenhouseSensor/logs/flaskServer_error.log"

# Activate virtual environment and start main.py
source /home/pi/Desktop/Greenhouse/GreenhouseSensor/.env/bin/activate
python3 /home/pi/Desktop/Greenhouse/GreenhouseSensor/main.py 2>> "$MAIN_PY_ERROR_LOG" &

# Start flaskServer.py
/usr/bin/python3 /home/pi/Desktop/Greenhouse/GreenhouseSensor/Webserver/flaskServer.py 2>> "$FLASK_SERVER_ERROR_LOG"

