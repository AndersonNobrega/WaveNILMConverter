#!/bin/bash

# Import functions and variables
. $HOME/ProgrammingProjects/College/DatasetConverter/scripts/util/functions.sh

# AMPDS
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --ampds --dat "$AMPDS_PATH" -m
deactivate_anaconda_env

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