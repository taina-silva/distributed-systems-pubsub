#!/bin/bash

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo apt-get update
    sudo apt-get install python-pi
fi

python3 -m pip install --upgrade pip
pip install -e .
pip install grpcio-tools
pip3 install "paho-mqtt<2.0.0"

chmod +x admin-client.sh
chmod +x admin-server.sh
chmod +x mat-client.sh
chmod +x mat-server.sh