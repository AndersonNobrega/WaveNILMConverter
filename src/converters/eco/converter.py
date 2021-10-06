from multiprocessing import Process
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup
from nilmtk import DataSet
from numpy import empty, copy
from pathlib import Path
from pickle import dump
from os import path


class EcoConverter():
    def __init__(self, dir_path, h5_file='/data/h5/ECO.h5', dat_path='/data/dat/eco'):
        self.h5_file = h5_file
        self.dat_path = dat_path
        self.dir_path = dir_path

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

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                values[i][1] = [row._1]  # 1 - Active Power
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        if not path.isdir(self.dir_path + self.dat_path + building_name):
            Path(self.dir_path + self.dat_path + building_name).mkdir(parents=True, exist_ok=True)
        dat_file = open(self.dir_path + self.dat_path + building_name + '/' + file_name, 'wb')

        file_values = empty((len(df), 3, 1))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row._1] # 1 - Active Power
        
        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

    def run_processes(self, df_list, df_aggregate, building_name):
        processes = list()
        for df, file_name in df_list:
            new_process = Process(target=self.create_dat_file, args=(df, df_aggregate, file_name, building_name))
            processes.append(new_process) # Save process to join later
            new_process.start()

        for process in processes:
            process.join()

    def convert_df(self):
        elec = self.read_dataset(self.dir_path + self.h5_file).buildings[1].elec

        df_aggregate = next(elec.mains().load())

        df_list = [
            [self.read_df(elec[4]), 'fridge.dat'],
            [self.read_df(elec[5]), 'hair_dryer.dat'],
            [self.read_df(elec[6]), 'coffee_maker.dat'],
            [self.read_df(elec[7]), 'kettle.dat'],
            [self.read_df(elec[8]), 'washing_machine.dat'],
            [self.read_df(elec[9]), 'computer.dat'],
            [self.read_df(elec[10]), 'freezer.dat'],
        ]

        self.run_processes(df_list, df_aggregate, '/building1')