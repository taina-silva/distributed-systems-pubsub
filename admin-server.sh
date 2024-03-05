#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/portal_administrativo/server.py
else
    python3 scripts/portal_administrativo/server.py $1
fi
