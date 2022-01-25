from os import path
from pickle import dump

from converters.base_converter import BaseConverter
from numpy import empty, copy, isnan


class IaweConverter(BaseConverter):
    def __init__(self, dir_path, h5_file='/data/h5/iAWE.h5', dat_path='/data/dat/iawe', measuraments=3, features=2,
                 single_loads=False, multiple_loads=False):
        super().__init__(dir_path, h5_file, dat_path, 0, measuraments, features, single_loads, multiple_loads)

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        last_values = [0, 0]
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                if isnan(row.active):
                    values[i][1] = [last_values[0] + values[i][2][0], last_values[1] + values[i][2][1]]
                else:
                    last_values = [row.active, row.reactive]
                    values[i][1] = [row.active, row.reactive]
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        dat_file = self.return_dat_file_path(self.dat_path, file_name)

        file_values = empty((len(df), self.measuraments, self.features))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row.active, row.reactive]

        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (self.dat_path + '/' + appliance_name + '.json'))

    def create_multiple_loads_file(self, df_aggregate, df_list, file_name, building_name):
        features_name = ['active', 'current', 'reactive', 'voltage']

        df_aggregate = self.rename_index(df_aggregate)
        for values in self.all_features_combinations(features_name):
            dat_file = self.return_dat_file_path(self.dat_path, '_'.join(values) + '_' + file_name)
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
                                 (self.dat_path + '/' + appliance_name + '.json'))

    def convert_df(self):
        elec = (list(self.read_dataset(self.dir_path + self.h5_file).buildings.values())[0]).elec

        if self.single_loads:
            df_aggregate = self.read_df(elec)['power']

            df_list = [
                [elec[3], 'fridge.dat'],
                [elec[4], 'air_conditioner_1.dat'],
                [elec[5], 'air_conditioner_2.dat'],
                [elec[6], 'washing_machine.dat'],
                [elec[7], 'laptop_computer.dat'],
                [elec[8], 'clothes_iron.dat'],
                [elec[9], 'kitchen_outlets.dat'],
                [elec[10], 'television.dat'],
                [elec[11], 'water_filter.dat'],
            ]

            self.run_processes(self.create_dat_file, df_list, df_aggregate, 'building1')

        if self.multiple_loads:
            df_multiple_loads = [
                elec[5],
                elec[4],
                elec[3],
                elec[7],
                elec[10]
            ]

            self.create_multiple_loads_file(self.read_df(elec), df_multiple_loads, 'iawe_5_loads.dat', 'building1')
