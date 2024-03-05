#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/portal_matricula/client.py
else
    python3 scripts/portal_matricula/client.py $1
fi
