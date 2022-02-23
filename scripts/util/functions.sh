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
    dataset=$5
    config=$6
    depth=$7
    sample_size=1440

    for filename in $data_path/*.dat; do
        data_len=`cat "$base_path"/$(basename "${filename%.*}").json | jq '.data_len'`
        result=$((($data_len + ($sample_size - 1)) / $sample_size))
        mkdir --parents $results_path/$epochs
        if [ $result -lt $SAMPLE_SIZE_LIMIAR ]; then
            sample_size=$((($data_len + ($SAMPLE_SIZE_LIMIAR - 1)) / $SAMPLE_SIZE_LIMIAR))
        fi
        (cd $WAVENILM_PATH/src
        python -m waveNILM with adam verbose=2 data_len=$data_len data_source=$(basename "$filename") dataset_name=$dataset agg_ind=[1] app_inds=[0,1,2,3,4] noise_mode=1 cross_validate=True n_epochs=$epochs val_spl=.15 splice=[1] batch_size=10 sample_size=$sample_size nb_filters=$config depth=$depth past_window_fraction=1.0 save_flag=False)
    done
}

move_dat_files() {
    data_path="$1"
    for filename in "$data_path"/*.dat; do
        mv "$filename" $WAVENILM_PATH/data
    done
}

remove_dat_files() {
    data_path="$1"
    for filename in "$data_path"/*.dat; do
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
EPOCHS=(120)
NB=([128,256,512,512,256,256])
DEPTH=(6)

# Filters configurations to try out:
# [512,128,128,128,1]
# [128,256,512,512,256,256]
# [64,128,256,256,512,512,512,512]
# [512,256,256,128,128,256,256,256,512]
