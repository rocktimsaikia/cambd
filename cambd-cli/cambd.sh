#!/usr/bin/bash

help() {
 echo "Cambridge dictionary cli app"
 echo
 echo "Usage:"
 echo "$ cambd <word>"
 echo
 echo "Options:"
 echo "--clean-cache	Clean the local cache."
 echo "--help		Print this help."
 echo
 echo "Examples:"
 echo "$ cambd neccessery"
 echo
}

if [ "$1" = "--clean-cache" ]; then
  rm -f ~/.cambd-cache
  exit
elif [ "$1" = "" ] || [ "$1" = "--help" ]; then
  help
  exit
fi

python3 /usr/local/src/cambd-cli/cambd.py "$1"
