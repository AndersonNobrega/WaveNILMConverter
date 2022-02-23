import logging
from os import path
from pickle import dump

from converters.base_converter import BaseConverter
from numpy import empty, isnan


class EcoConverter(BaseConverter):
    def __init__(self, dir_path, h5_file='/data/h5/ECO.h5', dat_path='/data/dat/eco', measuraments=3, features=1,
                 single_loads=False, multiple_loads=False):
        super().__init__(dir_path, h5_file, dat_path, 0, measuraments, features, single_loads, multiple_loads)

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        last_value = 0
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                if isnan(row.active):
                    values[i][1] = [last_value + values[i][2]]
                else:
                    last_value = row.active
                    values[i][1] = [row.active]
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        dat_file = self.return_dat_file_path(self.dat_path + building_name, file_name)

        file_values = empty((len(df), self.measuraments, self.features))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row.active]

        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df),
                             (self.dat_path + building_name + '/' + appliance_name + '.json'))

    def create_multiple_loads_file(self, df_aggregate, df_list, file_name, building_name):
        features_name = ['active']

        df_aggregate = self.rename_index(df_aggregate)
        for values in self.all_features_combinations(features_name):
            dat_file = self.return_dat_file_path(self.dat_path + '/' + building_name,
                                                 '_'.join(values) + '_' + file_name)
            file_values = empty((len(df_aggregate), len(df_list) + 2, len(values)))

            for i, row in enumerate(df_aggregate.itertuples()):
                file_values[i][1], file_values[i][0] = self.return_field_values(values, row)

            for appliance_index, df_meter in enumerate(df_list):
                df = self.rename_index(self.read_df(df_meter))
                df_iterator = df.itertuples()
                new_value = True
                value = 0
                i = 0
                while True:
                    if new_value:
                        row = next(df_iterator, None)
                        if row is None:
                            break
                        value, timestamp = self.return_field_values(values, row)
                        new_value = False

                    if timestamp[0] == file_values[i][0][0]:
                        file_values[i][appliance_index + 2] = value
                        new_value = True
                    else:
                        file_values[i][appliance_index + 2] = 0

                    i += 1

                    if len(file_values) <= i:
                        break

            dump(file_values, dat_file)
            dat_file.close()

            appliance_name = '_'.join(values) + '_' + path.splitext(file_name)[0]
            self.create_metadata(building_name, appliance_name, len(df_aggregate),
                                 (self.dat_path + '/' + building_name + '/' + appliance_name + '.json'))

    def single_loads_convert(self, buildings_list):
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building1')
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building2')
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building3')
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building4')
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building5')
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

                self.run_processes(self.create_dat_file, df_building, df_aggregate, '/building6')
                logging.info('Conversion from building 6 finished.')

    def multiple_loads_convert(self, buildings_list):
        for value in buildings_list:
            if value == 1:
                logging.info('Converting data from building 1... (Multiple Loads)')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[1].elec

                df_multiple_loads = [
                    elec[8],
                    elec[5],
                    elec[4],
                    elec[10],
                    elec[9]
                ]

                self.create_multiple_loads_file(self.read_df(elec), df_multiple_loads, 'eco_5_loads_building_1.dat',
                                                'building1')
            elif value == 2:
                logging.info('Converting data from building 2... (Multiple Loads)')
                elec = self.read_dataset(self.dir_path + self.h5_file).buildings[2].elec

                df_multiple_loads = [
                    elec[8],
                    elec[14],
                    elec[9],
                    elec[7],
                    elec[15]
                ]

                self.create_multiple_loads_file(self.read_df(elec), df_multiple_loads, 'eco_5_loads_building_2.dat',
                                                'building2')

    def convert_df(self, buildings_list):
        if self.single_loads:
            self.single_loads_convert(buildings_list)
        if self.multiple_loads:
            self.multiple_loads_convert(buildings_list)
