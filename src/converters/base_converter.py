import json
from multiprocessing import cpu_count, Pool
from os import path
from pathlib import Path

from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup
from numpy import empty
from pandas import DataFrame


class BaseConverter:
    def __init__(self, dir_path, h5_file, dat_path, data_len, measuraments, features):
        self.h5_file = h5_file
        self.dat_path = dat_path
        self.dir_path = dir_path
        self.data_len = data_len
        self.measuraments = measuraments
        self.features = features
        self.values = empty((data_len, measuraments, features))

    def return_dat_file_path(self, base_path, file_name):
        if not path.isdir(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)
        return open(base_path + '/' + file_name, 'wb')

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
        elif type(elec_meter) is ElecMeter:
            return next(elec_meter.load())

        raise TypeError('Data is not of a supported type')

    def create_metadata(self, building, appliance, data_len, path):
        data = {
            'building': building,
            'appliance': appliance,
            'data_len': data_len,
        }

        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def run_processes(self, method_reference, df_list, df_aggregate, building_name):
        pool = Pool(processes=cpu_count() // 3)
        for df, file_name in df_list:
            if type(df_aggregate) != DataFrame:
                pool.apply_async(method_reference, args=(self.read_df(df)['power'], file_name, building_name))
            else:
                pool.apply_async(method_reference,
                                    args=(self.read_df(df)['power'], df_aggregate, file_name, building_name))
        pool.close()
        pool.join()
