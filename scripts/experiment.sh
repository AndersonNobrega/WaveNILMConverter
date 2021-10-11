#!/bin/bash

wavenilm_env() {
    echo 'Changing to WaveNILM env'
    source $WAVENILM_PATH/bin/activate
}

anaconda_env() {
    echo 'Changing to Anaconda env'
    source $HOME/anaconda3/bin/activate
    conda activate nilmtk-practice
}

run_wavenilm() {
    wavenilm_env
    base_path=$1
    data_path=$2
    results_path=$3
    epochs=$4
    for filename in $data_path/*.dat; do
        data_len=`cat $base_path/$(basename "${filename%.*}").json | jq '.data_len'`
        mkdir --parents $results_path/$epochs
        (cd $WAVENILM_PATH/src
        python -m waveNILM with adam verbose=0 data_len=$data_len data_source=$(basename "$filename") acc_file=$results_path/$epochs/$(basename "${filename%.*}").json agg_ind=[1] app_inds=[0] noise_mode=1 cross_validate=True n_epochs=$epochs val_spl=.1 splice=[1] batch_size=5 nb_filters="[512, 128, 128, 128, 1]" depth=5 past_window_fraction=1.0)
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

WAVENILM_PATH=$HOME/envs/wavenilm
DATA_PATH=$WAVENILM_PATH/data
AMPDS_PATH=$HOME/ProgrammingProjects/College/DatasetConverter/data/dat/ampds/
AMPDS_RESULTS=$HOME/Documents/Results/AMPds

PYTHONPATH=$WAVENILM_PATH/src export PYTHONPATH
EPOCHS=(1 5 15 30)

# AMPDS
anaconda_env
python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py -a

move_dat_files $AMPDS_PATH

for epoch in "${EPOCHS[@]}"; do
    run_wavenilm $AMPDS_PATH $DATA_PATH $AMPDS_RESULTS $epoch
done

remove_dat_files $AMPDS_PATH

#python3 $HOME/ProgrammingProjects/College/DatasetConverter/src/main.py -e 1
#rm -rf $HOME/ProgrammingProjects/College/DatasetConverter/data/dat/eco/building1
