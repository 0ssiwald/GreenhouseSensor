#!/bin/bash

until python3 main.py; do
    echo "Server 'main.py' crashed with exit code $?. Respawning.." >&2
    sleep 1
done
