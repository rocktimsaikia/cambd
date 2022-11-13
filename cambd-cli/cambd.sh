#!/bin/sh
if [ "$1" = "--clean-cache" ]; then
  echo {} > ~/.cambd-cache.json
  exit
fi

python /usr/local/src/cambd-cli/cambd.py "$1"
