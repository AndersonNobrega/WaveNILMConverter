import json
import logging
from multiprocessing import cpu_count, Pool
from os import path
from pathlib import Path
from pickle import dump

import numpy as np
from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup


class EcoConverter:
    def __init__(self, dir_path, h5_file='/data/h5/ECO.h5', dat_path='/data/dat/eco', measuraments=3, features=1):
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
        elif type(elec_meter) is ElecMeter:
            return next(elec_meter.load())

        raise TypeError('Data is not of a supported type')

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        last_value = 0
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                if np.isnan(row.active):
                    values[i][1] = [last_value + values[i][2]]
                else:
                    last_value = row.active
                    values[i][1] = [row.active]
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        base_path = self.dir_path + self.dat_path + building_name
        if not path.isdir(base_path):
            Path(base_path).mkdir(parents=True, exist_ok=True)

        dat_file = open(base_path + '/' + file_name, 'wb')

        file_values = np.empty((len(df), self.measuraments, self.features))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row.active]

        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def run_processes(self, df_list, df_aggregate, building_name):
        pool = Pool(processes=cpu_count() // 3)
        for df, file_name in df_list:
            pool.apply_async(self.create_dat_file,
                             args=(self.read_df(df)['power'], df_aggregate, file_name, building_name))
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

    def convert_df(self, buildings_list):
        for value in buildings_list:
            if value == 1:
                logging.info('Converting data from building 1...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[1].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'fridge.dat'],
                    [elec[5], 'hair_dryer.dat'],
                    [elec[6], 'coffee_maker.dat'],
                    [elec[7], 'kettle.dat'],
                    [elec[8], 'washing_machine.dat'],
                    [elec[9], 'computer.dat'],
                    [elec[10], 'freezer.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building1')
                logging.info('Conversion from building 1 finished.')
            elif value == 2:
                logging.info('Converting data from building 2...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[2].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'tablet_computer_charger.dat'],
                    [elec[5], 'dish_washer.dat'],
                    [elec[6], 'air_handling_unit.dat'],
                    [elec[7], 'fridge.dat'],
                    [elec[8], 'HTPC.dat'],
                    [elec[9], 'freezer.dat'],
                    [elec[10], 'kettle.dat'],
                    [elec[11], 'lamp.dat'],
                    [elec[12], 'laptop_computer.dat'],
                    [elec[13], 'stove.dat'],
                    [elec[14], 'television.dat'],
                    [elec[15], 'audio_system.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building2')
                logging.info('Conversion from building 2 finished.')
            elif value == 3:
                logging.info('Converting data from building 3...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[3].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'laptop_computer.dat'],
                    [elec[5], 'freezer.dat'],
                    [elec[6], 'coffee_maker.dat'],
                    [elec[7], 'computer.dat'],
                    [elec[8], 'fridge.dat'],
                    [elec[9], 'kettle.dat'],
                    [elec[10], 'HTPC.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building3')
                logging.info('Conversion from building 3 finished.')
            elif value == 4:
                logging.info('Converting data from building 4...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[4].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'fridge.dat'],
                    [elec[5], 'small_cooking_appliance.dat'],
                    [elec[6], 'lamp.dat'],
                    [elec[7], 'laptop_computer.dat'],
                    [elec[8], 'freezer.dat'],
                    [elec[9], 'games_console.dat'],
                    [elec[10], 'HTPC.dat'],
                    [elec[11], 'microwave.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building4')
                logging.info('Conversion from building 4 finished.')
            elif value == 5:
                logging.info('Converting data from building 5...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[5].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'laptop_computer.dat'],
                    [elec[5], 'coffee_maker.dat'],
                    [elec[6], 'garden_sprinkler.dat'],
                    [elec[7], 'microwave.dat'],
                    [elec[8], 'fridge.dat'],
                    [elec[9], 'HTPC.dat'],
                    [elec[10], 'computer.dat'],
                    [elec[11], 'kettle.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building5')
                logging.info('Conversion from building 5 finished.')
            elif value == 6:
                logging.info('Converting data from building 6...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[6].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[4], 'lamp.dat'],
                    [elec[5], 'laptop_computer.dat'],
                    [elec[6], 'broadband_router.dat'],
                    [elec[7], 'coffee_maker.dat'],
                    [elec[8], 'HTPC.dat'],
                    [elec[9], 'fridge.dat'],
                    [elec[10], 'kettle.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building6')
                logging.info('Conversion from building 6 finished.')
