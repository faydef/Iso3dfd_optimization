#!/bin/bash

if [ -z "${1##*--parallel*}" ]; then
  echo "exécution en parallèle"
else
  python3 main.py "$@"
fi

