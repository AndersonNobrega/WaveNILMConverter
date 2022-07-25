#!/bin/bash

# Import functions and variables
. $CONVERTER_PATH/scripts/util/functions.sh

# AMPDS Variables
AMPDS_PATH="/media/anderson/HDD_Linux/data/dat/ampds"
AMPDS_RESULTS=$HOME/Documents/Results/AMPds
AMPDS_NAME=AMPds

# AMPDS
converter_env
python3 $CONVERTER_PATH/src/main.py --ampds --dat "$AMPDS_PATH" -s
deactivate_env

move_dat_files "$AMPDS_PATH"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$AMPDS_PATH" $DATA_PATH $AMPDS_RESULTS $epoch $AMPDS_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$AMPDS_PATH"
remove_sample_folders