#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/portal_administrativo/client.py
else
    python3 scripts/portal_administrativo/client.py $1
fi
