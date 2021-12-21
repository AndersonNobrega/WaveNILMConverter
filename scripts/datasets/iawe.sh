#!/bin/bash

# Import functions and variables
. $HOME/ProgrammingProjects/College/DatasetConverter/scripts/util/functions.sh

# iAWE
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --iawe --dat "$IAWE_PATH" -m
deactivate_anaconda_env

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