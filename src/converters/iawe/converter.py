import csv
from os import path
from pickle import dump

import numpy as np
from converters.base_converter import BaseConverter


class IaweConverter(BaseConverter):
    def __init__(self, dir_path, h5_file='/data/h5/iAWE.h5', dat_path='/data/dat/iawe', measuraments=3, features=2):
        super().__init__(dir_path, h5_file, dat_path, 0, measuraments, features)

    def populate_aggregate_data(self, df, values, max_len):
        i = 0
        last_values = [0, 0]
        for row in df.itertuples():
            if i >= max_len:
                break
            if row.Index.to_pydatetime().timestamp() == values[i][0][0]:
                if np.isnan(row.active):
                    values[i][1] = [last_values[0] + values[i][2][0], last_values[1] + values[i][2][1]]
                else:
                    last_values = [row.active, row.reactive]
                    values[i][1] = [row.active, row.reactive]
                i += 1

        return values

    def create_dat_file(self, df, df_aggregate, file_name, building_name):
        base_path = self.dir_path + self.dat_path
        dat_file = self.return_dat_file_path(base_path, file_name)

        file_values = np.empty((len(df), self.measuraments, self.features))

        for i, row in enumerate(df.itertuples()):
            file_values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            file_values[i][2] = [row.active, row.reactive]

        file_values = self.populate_aggregate_data(df_aggregate, file_values, len(df))

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def create_csv(self, df):
        with open('/home/anderson/Documents/40_ac.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')

            writer.writerow(['Timestamp', 'PT', 'PA', 'PB', 'PC', 'QT', 'QA', 'QB', 'QC', 'UrmsA'])
            for row in df:
                new_row = [row[0][0], row[2][0], row[2][0], 0, 0, row[2][1], row[2][1], 0, 0, row[2][2]]
                writer.writerow(new_row)

    def convert_df(self):
        elec = (list(self.read_dataset(self.dir_path + self.h5_file).buildings.values())[0]).elec

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
