#!/bin/bash

# Import functions and variables
. $CONVERTER_PATH/scripts/util/functions.sh

# iAWE Variables
IAWE_PATH="/media/anderson/HDD_Linux/data/dat/iawe"
IAWE_RESULTS=$HOME/Documents/Results/iawe
IAWE_NAME=iAWE

# iAWE
converter_env
python3 $CONVERTER_PATH/src/main.py --iawe --dat "$IAWE_PATH" -m
deactivate_env

move_dat_files "$IAWE_PATH"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$IAWE_PATH" $DATA_PATH $IAWE_RESULTS $epoch $IAWE_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$IAWE_PATH"
remove_sample_folders