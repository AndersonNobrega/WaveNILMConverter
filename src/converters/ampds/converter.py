from multiprocessing import Process
from nilmtk.metergroup import MeterGroup
from nilmtk import DataSet
from numpy import empty, copy
from pathlib import Path
from pickle import dump
from os import path

import json


class AmpdsConverter():
    def __init__(self, dir_path, h5_file='/data/h5/AMPds2.h5', dat_path='/data/dat/ampds', data_len=1051200, measuraments=3, features=2):
        self.h5_file = h5_file
        self.dat_path = dat_path
        self.dir_path = dir_path
        self.values = empty((data_len, measuraments, features))

    def read_dataset(self, file):
        if Path(file).is_file():
            return DataSet(file)

        raise IOError('Path provided no file')

    def read_df(self, elec_meter, appliance=None):
        if type(elec_meter) is MeterGroup:
            if appliance is not None:
                return next(elec_meter[appliance].load())
            else:
                return next(elec_meter.mains().load())

        raise TypeError('Data is not of a supported type')

    def populate_aggregate_data(self, df):
        for i, row in enumerate(df.itertuples()):
            self.values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            self.values[i][1] = [row._4, row._1]  # 4 - Active Power, 1 - Reactive Power

    def create_dat_file(self, df, file_name):
        base_path = self.dir_path + self.dat_path
        if not path.isdir(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)
        dat_file = open(base_path + '/' + file_name, 'wb')

        file_values = copy(self.values)

        for i, row in enumerate(df.itertuples()):
            file_values[i][2] = [row._4, row._1] # 4 - Active Power, 1 - Reactive Power

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata('building1', appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def run_processes(self, df_list):
        processes = list()
        for df, file_name in df_list:
            new_process = Process(target=self.create_dat_file, args=(df, file_name))
            processes.append(new_process) # Save process to join later
            new_process.start()

        for process in processes:
            process.join()

    def create_metadata(self, building, appliance, data_len, path):
        data = {
            'building': building,
            'appliance': appliance,
            'data_len': data_len,
        }

        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def convert_df(self):
        elec = (list(self.read_dataset(self.dir_path + self.h5_file).buildings.values())[0]).elec

        df_list = [
            [self.read_df(elec, 'light'), 'light.dat'],
            [self.read_df(elec, 'unknown'), 'unknown.dat'],
            [self.read_df(elec, 'sockets'), 'sockets.dat'],
            [self.read_df(elec, 'fridge'), 'fridge.dat'],
            [self.read_df(elec, 'heat pump'), 'heat_pump.dat'],
            [self.read_df(elec, 'television'), 'television.dat'],
            [self.read_df(elec, 'electric oven'), 'electric_oven.dat'],
        ]

        self.populate_aggregate_data(self.read_df(elec))

        self.run_processes(df_list)
