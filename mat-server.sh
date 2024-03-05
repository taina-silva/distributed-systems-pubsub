#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/portal_matricula/server.py
else
    python3 scripts/portal_matricula/server.py $1
fi
