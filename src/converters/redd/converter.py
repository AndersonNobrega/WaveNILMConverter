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


class ReddConverter:
    def __init__(self, dir_path, h5_file='/data/h5/REDD.h5', dat_path='/data/dat/red', measuraments=3, features=1):
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
            file_values[i][2] = [row.apparent]

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
        # TODO: Verificar por NaN nos agregado

        for value in buildings_list:
            if value == 1:
                logging.info('Converting data from building 1...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[1].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec.nested_metergroups()[0], 'electric_oven.dat'],
                    [elec[5], 'fridge.dat'],
                    [elec[6], 'dish_washer.dat'],
                    [elec[7], 'kitchen_outlets_1.dat'],
                    [elec[8], 'kitchen_outlets_2.dat'],
                    [elec[9], 'light_1.dat'],
                    [elec.nested_metergroups()[1], 'washer_dryer.dat'],
                    [elec[11], 'microwave.dat'],
                    [elec[12], 'bathroom_gfi.dat'],
                    [elec[13], 'electric_space_heater.dat'],
                    [elec[14], 'electric_stove.dat'],
                    [elec[15], 'kitchen_outlets_3.dat'],
                    [elec[16], 'kitchen_outlets_4.dat'],
                    [elec[17], 'light_2.dat'],
                    [elec[18], 'light_3.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building1')
                logging.info('Conversion from building 1 finished.')
            elif value == 2:
                logging.info('Converting data from building 2...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[2].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[3], 'kitchen_outlets_1.dat'],
                    [elec[4], 'light_1.dat'],
                    [elec[5], 'electric_oven.dat'],
                    [elec[6], 'microwave.dat'],
                    [elec[7], 'washer_dryer.dat'],
                    [elec[8], 'kitchen_outlets_2.dat'],
                    [elec[9], 'fridge.dat'],
                    [elec[10], 'dish_washer.dat'],
                    [elec[11], 'waste_disposal_unit.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building2')
                logging.info('Conversion from building 2 finished.')
            elif value == 3:
                logging.info('Converting data from building 3...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[3].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[3], 'outlets_unknown_1.dat'],
                    [elec[4], 'outlets_unknown_2.dat'],
                    [elec[5], 'light_1.dat'],
                    [elec[6], 'ce_appliance.dat'],
                    [elec[7], 'fridge.dat'],
                    [elec[8], 'waste_disposal_unit.dat'],
                    [elec[9], 'dish_washer.dat'],
                    [elec[10], 'electric_furnace.dat'],
                    [elec[11], 'light_2.dat'],
                    [elec[12], 'outlets_unknown_3.dat'],
                    [elec.nested_metergroups()[0], 'washer_dryer.dat'],
                    [elec[15], 'light_3.dat'],
                    [elec[16], 'microwave.dat'],
                    [elec[17], 'light_4.dat'],
                    [elec[18], 'smoke_alarms.dat'],
                    [elec[19], 'light_5.dat'],
                    [elec[20], 'bathroom_gfi.dat'],
                    [elec[21], 'kitchen_outlets_1.dat'],
                    [elec[22], 'kitchen_outlets_2.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building3')
                logging.info('Conversion from building 3 finished.')
            elif value == 4:
                logging.info('Converting data from building 4...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[4].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[3], 'light_1.dat'],
                    [elec[4], 'electric_furnace.dat'],
                    [elec[5], 'kitchen_outlets_1.dat'],
                    [elec[6], 'outlets_unknown_1.dat'],
                    [elec[7], 'washer_dryer.dat'],
                    [elec[8], 'electric_stove.dat'],
                    [elec.nested_metergroups()[0], 'air_conditioner_1.dat'],
                    [elec[11], 'miscellaeneous.dat'],
                    [elec[12], 'smoke_alarms.dat'],
                    [elec[13], 'light_2.dat'],
                    [elec[14], 'kitchen_outlets_2.dat'],
                    [elec[15], 'dish_washer.dat'],
                    [elec[16], 'bathroom_gfi_1.dat'],
                    [elec[17], 'bathroom_gfi_2.dat'],
                    [elec[18], 'light_3.dat'],
                    [elec[19], 'light_4.dat'],
                    [elec[20], 'air_conditioner_2.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building4')
                logging.info('Conversion from building 4 finished.')
            elif value == 5:
                logging.info('Converting data from building 5...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[5].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[3], 'microwave.dat'],
                    [elec[4], 'light_1.dat'],
                    [elec[5], 'outlets_unknown_1.dat'],
                    [elec[6], 'electric_furnace.dat'],
                    [elec[7], 'outlets_unknown_2.dat'],
                    [elec.nested_metergroups()[0], 'washer_dryer.dat'],
                    [elec[10], 'subpanel_1.dat'],
                    [elec[11], 'subpanel_2.dat'],
                    [elec.nested_metergroups()[1], 'electric_space_heater.dat'],
                    [elec[14], 'light_2.dat'],
                    [elec[15], 'outlets_unknown_3.dat'],
                    [elec[16], 'bathroom_gfi_1.dat'],
                    [elec[17], 'light_3.dat'],
                    [elec[18], 'fridge.dat'],
                    [elec[19], 'light_4.dat'],
                    [elec[20], 'dish_washer.dat'],
                    [elec[21], 'waste_disposal_unit.dat'],
                    [elec[22], 'ce_appliance.dat'],
                    [elec[23], 'light_5.dat'],
                    [elec[24], 'kitchen_outlets_1.dat'],
                    [elec[25], 'kitchen_outlets_2.dat'],
                    [elec[26], 'outdoor_outlets_1.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building5')
                logging.info('Conversion from building 5 finished.')
            elif value == 6:
                logging.info('Converting data from building 6...')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[6].elec
                df_aggregate = next(elec.mains().load())['power']

                df_building = [
                    [elec[3], 'kitchen_outlets_1.dat'],
                    [elec[4], 'washer_dryer.dat'],
                    [elec[5], 'electric_stove.dat'],
                    [elec[6], 'ce_appliance.dat'],
                    [elec[7], 'bathroom_gfi_1.dat'],
                    [elec[8], 'fridge.dat'],
                    [elec[9], 'dish_washer.dat'],
                    [elec[10], 'outlets_unknown_1.dat'],
                    [elec[11], 'outlets_unknown_2.dat'],
                    [elec[12], 'electric_space_heater.dat'],
                    [elec[13], 'kitchen_outlets_2.dat'],
                    [elec[14], 'light_1.dat'],
                    [elec[15], 'air_handling_unit.dat'],
                    [elec.nested_metergroups()[0], 'air_conditioner.dat'],
                ]

                self.run_processes(df_building, df_aggregate, '/building6')
                logging.info('Conversion from building 6 finished.')
