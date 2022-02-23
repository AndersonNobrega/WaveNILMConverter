import json
from itertools import combinations
from multiprocessing import cpu_count, Pool
from os import path
from pathlib import Path

from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup
from numpy import empty, isnan
from pandas import DataFrame


class BaseConverter:
    def __init__(self, dir_path, h5_file, dat_path, data_len, measuraments, features, single_loads, multiple_loads):
        self.h5_file = h5_file
        self.dat_path = dat_path
        self.dir_path = dir_path
        self.data_len = data_len
        self.measuraments = measuraments
        self.features = features
        self.values = empty((data_len, measuraments, features))
        self.single_loads = single_loads
        self.multiple_loads = multiple_loads

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

    def all_features_combinations(self, features_list):
        all_combinations = []
        for r in range(len(features_list) + 1):
            combinations_object = combinations(features_list, r)
            for x in list(combinations_object):
                if len(x) != 0:
                    if (len(x) == 1 and ('voltage' in x or 'reactive' in x)) or set(x) == set(['reactive', 'voltage']):
                        continue
                    else:
                        all_combinations.append(list(x))

        return all_combinations

    def rename_index(self, df):
        columns_name = []
        for col in df.columns.values:
            columns_name.append([str(value) for value in col if str(value) != 'nan'])

        for i, name in enumerate(columns_name):
            if 'voltage' in name and len(name) > 1:
                columns_name[i] = ['voltage']
            elif 'current' in name and len(name) > 1:
                columns_name[i] = ['current']

        df.columns = [' '.join(col).strip() for col in columns_name]
        df.columns = df.columns.str.replace(' ', '_')

        return df

    def return_field_values(self, features_list, row):
        values_row = []
        timestamp_row = []
        if 'apparent' in features_list:
            if isnan(row.power_apparent):
                values_row.append(0)
            else:
                values_row.append(row.power_apparent)
            timestamp_row.append(row.Index.to_pydatetime().timestamp())
        if 'active' in features_list:
            if isnan(row.power_active):
                values_row.append(0)
            else:
                values_row.append(row.power_active)
            timestamp_row.append(row.Index.to_pydatetime().timestamp())
        if 'current' in features_list:
            if isnan(row.current):
                values_row.append(0)
            else:
                values_row.append(row.current)
            timestamp_row.append(row.Index.to_pydatetime().timestamp())
        if 'reactive' in features_list:
            if isnan(row.power_reactive):
                values_row.append(0)
            else:
                values_row.append(row.power_reactive)
            timestamp_row.append(row.Index.to_pydatetime().timestamp())
        if 'voltage' in features_list:
            if isnan(row.voltage):
                values_row.append(0)
            else:
                values_row.append(row.voltage)
            timestamp_row.append(row.Index.to_pydatetime().timestamp())

        return values_row, timestamp_row

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
