#!/bin/bash

sleep 10
python3 /home/provision/girder.py
cd /home/data && python3 ingest.py ./data girder 8080 admin letmein
cd /home/data && python3 ingest_1000.py ./data girder 8080 admin letmein
