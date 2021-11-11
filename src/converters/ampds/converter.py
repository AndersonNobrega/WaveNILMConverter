import json
from multiprocessing import Process
from os import path
from pathlib import Path
from pickle import dump

from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup
from numpy import empty, copy


class AmpdsConverter:
    def __init__(self, dir_path, h5_file='/data/h5/AMPds2.h5', dat_path='/data/dat/ampds', data_len=1051200,
                 measuraments=3, features=2):
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
        elif type(elec_meter) is ElecMeter:
            return next(elec_meter.load())

        raise TypeError('Data is not of a supported type')

    def populate_aggregate_data(self, df):
        for i, row in enumerate(df.itertuples()):
            self.values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            self.values[i][1] = [row.active, row.reactive]

    def create_dat_file(self, df, file_name, building_name):
        base_path = self.dir_path + self.dat_path
        if not path.isdir(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)
        dat_file = open(base_path + '/' + file_name, 'wb')

        file_values = copy(self.values)

        for i, row in enumerate(df.itertuples()):
            file_values[i][2] = [row.active, row.reactive]

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def run_processes(self, df_list, building_name):
        processes = list()
        for df, file_name in df_list:
            new_process = Process(target=self.create_dat_file,
                                  args=(self.read_df(df)['power'], file_name, building_name))
            processes.append(new_process)  # Save process to join later
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
            [elec[2], 'north_bedroom.dat'],
            [elec[3], 'master_bedroom.dat'],
            [elec[4], 'partial_plugs.dat'],
            [elec[5], 'clothes_dryer.dat'],
            [elec[6], 'clothes_washer.dat'],
            [elec[7], 'dining_room_plugs.dat'],
            [elec[8], 'dishwasher.dat'],
            [elec[9], 'eletronics_workbench.dat'],
            [elec[10], 'security_network_equipment.dat'],
            [elec[11], 'air_furnace_thermostat.dat'],
            [elec[12], 'sub_panel.dat'],
            [elec[13], 'heat_pump.dat'],
            [elec[14], 'hot_water_unit.dat'],
            [elec[15], 'home_office.dat'],
            [elec[16], 'outside_plugs.dat'],
            [elec[17], 'panel_basement.dat'],
            [elec[18], 'entertainment.dat'],
            [elec[19], 'utility_plug.dat'],
            [elec[20], 'electric_oven.dat'],
        ]

        self.populate_aggregate_data(self.read_df(elec)['power'])

        self.run_processes(df_list, 'building1')
