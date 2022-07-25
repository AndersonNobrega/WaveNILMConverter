#!/bin/bash

# Get absolute path to this script
SCRIPT=$(readlink -f "$0")

# Get only the directory path
SCRIPTPATH=$(dirname "$SCRIPT")

# Project Path
CONVERTER_PATH=$HOME/ProgrammingProjects/College/DatasetConverter/

while [[ $# -gt 0 ]]
do
    case "$1" in
        --ampds)
            $SCRIPTPATH/datasets/ampds.sh
            ;;
        --eco)
            $SCRIPTPATH/datasets/eco.sh
            ;;
        --iawe)
            $SCRIPTPATH/datasets/iawe.sh
            ;;
        --redd)
            $SCRIPTPATH/datasets/redd.sh
            ;;
    esac
    shift
done