from multiprocessing import cpu_count, Pool
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup
from nilmtk import DataSet
from pathlib import Path
from pickle import dump
from os import path

import numpy as np
import json

class IaweConverter():
    def __init__(self, dir_path, h5_file='/data/h5/iAWE.h5', dat_path='/data/dat/iawe', measuraments=3, features=2):
        self.h5_file = h5_file
        self.dat_path = dat_path
        self.dir_path = dir_path
        self.measuraments = measuraments
        self.features = features

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

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                values[i][1] = [row.active, row.reactive]
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        base_path = self.dir_path + self.dat_path
        if not path.isdir(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)

        dat_file = open(base_path + '/' + file_name, 'wb')

        file_values = np.empty((len(df), self.measuraments, self.features))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row.active, row.reactive]

        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def run_processes(self, df_list, df_aggregate, building_name):
        pool = Pool(processes=cpu_count() // 3)
        for df, file_name in df_list:
            pool.apply_async(self.create_dat_file, args=(df, df_aggregate, file_name, building_name))
        pool.close()
        pool.join()

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
            [self.read_df(elec, 'fridge')['power'], 'fridge.dat'],
            [self.read_df(elec, 'air conditioner')['power'], 'air_conditioner.dat'],
            [self.read_df(elec, 'washing machine')['power'], 'washing_machine.dat'],
            [self.read_df(elec, 'computer')['power'], 'computer.dat'],
            [self.read_df(elec, 'clothes iron')['power'], 'clothes_iron.dat'],
            [self.read_df(elec, 'unknown')['power'], 'unknown.dat'],
            [self.read_df(elec, 'television')['power'], 'television.dat'],
            [self.read_df(elec, 'wet appliance')['power'], 'wet_appliance.dat'],
        ]

        self.run_processes(df_list, self.read_df(elec)['power'], 'building1')
