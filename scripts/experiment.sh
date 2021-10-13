#!/bin/bash

wavenilm_env() {
    echo 'Changing to WaveNILM env'
    source $WAVENILM_PATH/bin/activate
}

deactivate_env() {
    deactivate
}

anaconda_env() {
    echo 'Changing to Anaconda env'
    source $HOME/anaconda3/bin/activate
    conda activate nilmtk-practice
}

deactivate_anaconda_env() {
    conda deactivate
}

run_wavenilm() {
    base_path=$1
    data_path=$2
    results_path=$3
    epochs=$4
    sample_size=1440
    for filename in $data_path/*.dat; do
        data_len=`cat $base_path/$(basename "${filename%.*}").json | jq '.data_len'`
        result=$((($data_len + ($sample_size - 1)) / $sample_size))
        mkdir --parents $results_path/$epochs
        if [ $result -lt $SAMPLE_SIZE_LIMIAR ]; then
            sample_size=$((($data_len + ($SAMPLE_SIZE_LIMIAR - 1)) / $SAMPLE_SIZE_LIMIAR))
        fi
        (cd $WAVENILM_PATH/src
        python -m waveNILM with adam verbose=0 data_len=$data_len data_source=$(basename "$filename") acc_file=$results_path/$epochs/$(basename "${filename%.*}").json agg_ind=[1] app_inds=[0] noise_mode=1 cross_validate=True n_epochs=$epochs val_spl=.1 splice=[1] batch_size=5 sample_size=$sample_size nb_filters="[512, 128, 128, 128, 1]" depth=5 past_window_fraction=1.0 save_flag=False)
    done
}

move_dat_files() {
    data_path=$1
    for filename in $data_path/*.dat; do
        mv $filename $WAVENILM_PATH/data
    done
}

remove_dat_files() {
    data_path=$1
    for filename in $data_path/*.dat; do
        rm -rf $WAVENILM_PATH/data/$(basename "$filename")
    done
}

remove_sample_folders() {
    for file in $WAVENILM_PATH/data/*; do
        if [ -d "$file" ]; then
            folder=$(basename "$file")
            if [[ $folder == sample_size_* ]]; then
                rm -rf $file
            fi
        fi
    done
}

# Constants
SAMPLE_SIZE_LIMIAR=50
WAVENILM_PATH=$HOME/envs/wavenilm
DATA_PATH=$WAVENILM_PATH/data
PYTHONPATH=$WAVENILM_PATH/src export PYTHONPATH
EPOCHS=(1 5)

# AMPDS Variables
AMPDS_PATH=$HOME/ProgrammingProjects/College/DatasetConverter/data/dat/ampds
AMPDS_RESULTS=$HOME/Documents/Results/AMPds

# ECO Variables
ECO_PATH=$HOME/ProgrammingProjects/College/DatasetConverter/data/dat/eco
ECO_RESULTS=$HOME/Documents/Results/eco

# iAWE Variables
IAWE_PATH=$HOME/ProgrammingProjects/College/DatasetConverter/data/dat/iawe
IAWE_RESULTS=$HOME/Documents/Results/iawe

# AMPDS
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --ampds
deactivate_anaconda_env

move_dat_files $AMPDS_PATH

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    run_wavenilm $AMPDS_PATH $DATA_PATH $AMPDS_RESULTS $epoch
done
deactivate_env

remove_dat_files $AMPDS_PATH
remove_sample_folders

# ECO
# Building 1
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --eco 1
deactivate_anaconda_env

move_dat_files $ECO_PATH/building1

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    run_wavenilm $ECO_PATH/building1 $DATA_PATH $ECO_RESULTS/building1 $epoch
done
deactivate_env

remove_dat_files $ECO_PATH/building1
remove_sample_folders

# Building 2
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --eco 2
deactivate_anaconda_env

move_dat_files $ECO_PATH/building2

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    run_wavenilm $ECO_PATH/building2 $DATA_PATH $ECO_RESULTS/building2 $epoch
done
deactivate_env

remove_dat_files $ECO_PATH/building2
remove_sample_folders

# iAWE
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py --iawe
deactivate_anaconda_env

move_dat_files $IAWE_PATH

wavenilm_env
for epoch in "${EPOCHS[@]}"; do
    run_wavenilm $IAWE_PATH $DATA_PATH $IAWE_RESULTS $epoch
done
deactivate_env

remove_dat_files $IAWE_PATH
remove_sample_folders