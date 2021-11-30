from os import path
from pickle import dump

from converters.base_converter import Converter
from numpy import empty, copy


class AmpdsConverter(Converter):
    def __init__(self, dir_path, h5_file='/data/h5/AMPds2.h5', dat_path='/data/dat/ampds', data_len=1051200,
                 measuraments=3, features=2):
        super().__init__(dir_path, h5_file, dat_path, data_len, measuraments, features)

    def populate_aggregate_data(self, df):
        for i, row in enumerate(df.itertuples()):
            self.values[i][0] = [row.Index.to_pydatetime().timestamp(), row.Index.to_pydatetime().timestamp()]
            self.values[i][1] = [row.active, row.reactive]

    def create_dat_file(self, df, file_name, building_name):
        base_path = self.dir_path + self.dat_path
        dat_file = self.return_dat_file_path(base_path, file_name)

        file_values = copy(self.values)

        for i, row in enumerate(df.itertuples()):
            file_values[i][2] = [row.active, row.reactive]

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, len(df), (base_path + '/' + appliance_name + '.json'))

    def create_multiple_loads_file(self, df_list, file_name, building_name):
        base_path = self.dir_path + self.dat_path
        dat_file = self.return_dat_file_path(base_path, file_name)

        file_values = empty((self.data_len, len(df_list) + 2, self.features))
        file_values[:, :self.measuraments, :] = copy(self.values)

        for appliance_index, df_meter in enumerate(df_list):
            df = self.read_df(df_meter)['power']
            for i, row in enumerate(df.itertuples()):
                file_values[i][appliance_index + 2] = [row.active, row.reactive]

        dump(file_values, dat_file)
        dat_file.close()

        appliance_name = path.splitext(file_name)[0]
        self.create_metadata(building_name, appliance_name, self.data_len, (base_path + '/' + appliance_name + '.json'))

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

        self.run_processes(self.create_dat_file, df_list, None, 'building1')

