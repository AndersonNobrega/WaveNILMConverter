#!/bin/bash

# Import functions and variables
. $CONVERTER_PATH/scripts/util/functions.sh

# ECO Variables
ECO_PATH="/media/anderson/HDD_Linux/data/dat/eco"
ECO_RESULTS=$HOME/Documents/Results/eco
ECO_NAME=ECO

# ECO
# Building 1
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 1 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building1"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building1" $DATA_PATH $ECO_RESULTS/building1 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building1"
remove_sample_folders

# Building 2
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 2 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building2"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building2" $DATA_PATH $ECO_RESULTS/building2 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building2"
remove_sample_folders

# Building 3
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 3 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building3"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building3" $DATA_PATH $ECO_RESULTS/building3 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building3"
remove_sample_folders

# Building 4
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 4 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building4"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building4" $DATA_PATH $ECO_RESULTS/building4 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building4"
remove_sample_folders

# Building 5
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 5 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building5"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building5" $DATA_PATH $ECO_RESULTS/building5 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building5"
remove_sample_folders

# Building 6
converter_env
python3 $CONVERTER_PATH/src/main.py --eco 6 --dat "$ECO_PATH" -m
deactivate_env

move_dat_files "$ECO_PATH/building6"

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    for (( i = 0; i < ${#NB[@]}; i++ )); do
        run_wavenilm "$ECO_PATH/building6" $DATA_PATH $ECO_RESULTS/building6 $epoch $ECO_NAME ${NB[i]} ${DEPTH[i]}
    done
done
deactivate_env

remove_dat_files "$ECO_PATH/building6"
remove_sample_folders