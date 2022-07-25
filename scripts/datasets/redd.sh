#!/bin/bash

# Import functions and variables
. $CONVERTER_PATH/scripts/util/functions.sh

# REDD Variables
REDD_PATH="/media/anderson/HDD_Linux/data/dat/redd"
REDD_RESULTS=$HOME/Documents/Results/redd
REDD_NAME=REDD

# REDD
# Building 1
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 1 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building1"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building1" $DATA_PATH $REDD_RESULTS/building6 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building1"
remove_sample_folders

# Building 2
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 2 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building2"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building2" $DATA_PATH $REDD_RESULTS/building2 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building2"
remove_sample_folders

# Building 3
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 3 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building3"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building3" $DATA_PATH $REDD_RESULTS/building3 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building3"
remove_sample_folders

# Building 4
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 4 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building4"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building4" $DATA_PATH $REDD_RESULTS/building4 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building4"
remove_sample_folders

# Building 5
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 5 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building5"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building5" $DATA_PATH $REDD_RESULTS/building5 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building5"
remove_sample_folders

# Building 6
converter_env
python3 $CONVERTER_PATH/src/main.py --redd 6 --dat "$REDD_PATH" -m
deactivate_env

move_dat_files "$REDD_PATH/building6"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$REDD_PATH/building6" $DATA_PATH $REDD_RESULTS/building6 $epoch $REDD_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$REDD_PATH/building6"
remove_sample_folders