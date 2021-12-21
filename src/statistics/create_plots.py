from os import getenv, makedirs
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeter
from nilmtk.metergroup import MeterGroup

mpl.rcParams['agg.path.chunksize'] = 10000


def read_df(elec_meter, nested_meter=False):
    if type(elec_meter) is MeterGroup:
        if nested_meter == True:
            return next(elec_meter.load())
        else:
            return next(elec_meter.mains().load())
    elif type(elec_meter) is ElecMeter:
        return next(elec_meter.load())

    raise TypeError('Data is not of a supported type')


def read_dataset(file):
    if Path(file).is_file():
        return DataSet(file)

    raise IOError('Path provided no file')


def plot_line_graph(values, y_label, y_max, y_min, title, path):
    plt.subplots(figsize=(16, 10))
    plt.grid(True)
    plt.ylabel(y_label)
    plt.xlabel("Timestamp")
    plt.ylim(y_min, y_max)
    plt.title(title)
    plt.plot(values)
    plt.savefig(path, format='png', dpi=300)
    plt.clf()
    plt.close()


def create_plot(df_list, plot_path, dataset_name):
    min_samples = 11000
    for df, file_name, title, nested_meter in df_list:
        df = read_df(df, nested_meter)['power']

        if 'apparent' in df:
            df = df.drop('apparent', 1)

        if 'reactive' in df:
            df_active = df.drop('reactive', 1)
        else:
            df_active = df

        if 'active' in df:
            df_reactive = df.drop('active', 1)
        else:
            df_reactive = df

        try:
            makedirs(plot_path + '/Ativa/' + title)
            makedirs(plot_path + '/Reativa/' + title)
        except FileExistsError:
            pass

        if 'active' in df_active:
            max_value = df_active['active'].max()
            min_value = df_active['active'].min()
            split_value = len(df_active) // min_samples + 1
        
            for i, df_active_split in enumerate(np.array_split(df_active, split_value)):
                if i > 40:
                    break
                try:
                    plot_line_graph(df_active_split, 'Potência Ativa (W)', max_value, min_value, dataset_name + title, plot_path + '/Ativa/' + title + '/split_' + str(i) + '_' + file_name)
                except OverflowError:
                    continue
            try:
                plot_line_graph(df_active, 'Potência Ativa (W)', max_value, min_value, dataset_name + title, plot_path + '/Ativa/' + file_name)
            except OverflowError:
                continue
        if 'reactive' in df_reactive:
            max_value = df_reactive['reactive'].max()
            min_value = df_reactive['reactive'].min()
            split_value = len(df_reactive) // min_samples + 1

            for i, df_reactive_split in enumerate(np.array_split(df_reactive, split_value)):
                if i > 40:
                    break
                try:
                    plot_line_graph(df_reactive_split, 'Potência Reativa (W)', max_value, min_value, dataset_name + title, plot_path + '/Reativa/' + title + '/split_' + str(i) + '_' + file_name)
                except OverflowError:
                    continue
            try:
                plot_line_graph(df_reactive, 'Potência Reativa (W)', max_value, min_value, dataset_name + title, plot_path + '/Reativa/' + file_name)
            except OverflowError:
                continue

def ampds_data_plots(path, plot_path):
    ampds_elec = (list(read_dataset(path).buildings.values())[0]).elec

    df_list = [
        [ampds_elec, 'agregado.png', 'Agregado', False],
        [ampds_elec[2], 'north_bedroom.png', 'North Bedroom', False],
        [ampds_elec[3], 'master_bedroom.png', 'Master Bedroom', False],
        [ampds_elec[4], 'partial_plugs.png', 'Partial Plugs', False],
        [ampds_elec[5], 'clothes_dryer.png', 'Clothes Dryer', False],
        [ampds_elec[6], 'clothes_washer.png', 'Clothes Washer', False],
        [ampds_elec[7], 'dining_room_plugs.png', 'Dining Room Plugs', False],
        [ampds_elec[8], 'dishwasher.png', 'Dishwasher', False],
        [ampds_elec[9], 'eletronics_workbench.png', 'Eletronics Workbench', False],
        [ampds_elec[10], 'security_network_equipment.png', 'Security Network Equipment', False],
        [ampds_elec[11], 'air_furnace_thermostat.png', 'Air Furnace Thermostat', False],
        [ampds_elec[12], 'sub_panel.png', 'Sub Panel', False],
        [ampds_elec[13], 'heat_pump.png', 'Heat Pump', False],
        [ampds_elec[14], 'hot_water_unit.png', 'Hot Water Unit', False],
        [ampds_elec[15], 'home_office.png', 'Home Office', False],
        [ampds_elec[16], 'outside_plugs.png', 'Outside Plugs', False],
        [ampds_elec[17], 'panel_basement.png', 'Panel Basement', False],
        [ampds_elec[18], 'entertainment.png', 'Entertainment', False],
        [ampds_elec[19], 'utility_plug.png', 'Utility Plug', False],
        [ampds_elec[20], 'electric_oven.png', 'Electric Oven', False],
    ]

    create_plot(df_list, plot_path, 'AMPds - ')


def iawe_data_plots(path, plot_path):
    iawe_elec = (list(read_dataset(path).buildings.values())[0]).elec

    df_list = [
        [iawe_elec, 'agregado.png', 'Agregado', False],
        [iawe_elec[3], 'fridge.png', 'Fridge', False],
        [iawe_elec[4], 'air_conditioner_1.png', 'Air Conditioner 1', False],
        [iawe_elec[5], 'air_conditioner_2.png', 'Air Conditioner 2', False],
        [iawe_elec[6], 'washing_machine.png', 'Washing Machine', False],
        [iawe_elec[7], 'laptop_computer.png', 'Laptop Computer', False],
        [iawe_elec[8], 'clothes_iron.png', 'Clothes Iron', False],
        [iawe_elec[9], 'kitchen_outlets.png', 'Kitchen Outlets', False],
        [iawe_elec[10], 'television.png', 'Television', False],
        [iawe_elec[11], 'water_filter.png', 'Water Filter', False],
    ]

    create_plot(df_list, plot_path, 'iAWE - ')


def eco_data_plots(path, plot_path):
    eco_elec = read_dataset(path).buildings[1].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'fridge.png', 'Fridge', False],
        [eco_elec[5], 'hair_dryer.png', 'Hair Dryer', False],
        [eco_elec[6], 'coffee_maker.png', 'Coffee Maker', False],
        [eco_elec[7], 'kettle.png', 'Kettle', False],
        [eco_elec[8], 'washing_machine.png', 'Washing Machine', False],
        [eco_elec[9], 'computer.png', 'Computer', False],
        [eco_elec[10], 'freezer.png', 'Freezer', False],
    ]

    create_plot(df_list, plot_path + '/Building_1', 'ECO - Building 1 - ')

    eco_elec = read_dataset(path).buildings[2].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'tablet_computer_charger.png', 'Tablet Computer Charger', False],
        [eco_elec[5], 'dish_washer.png', 'Dish Washer', False],
        [eco_elec[6], 'air_handling_unit.png', 'Air Handling Unit', False],
        [eco_elec[7], 'fridge.png', 'Fridge', False],
        [eco_elec[8], 'HTPC.png', 'HTPC', False],
        [eco_elec[9], 'freezer.png', 'Freezer', False],
        [eco_elec[10], 'kettle.png', 'Kettle', False],
        [eco_elec[11], 'lamp.png', 'Lamp', False],
        [eco_elec[12], 'laptop_computer.png', 'Laptop Computer', False],
        [eco_elec[13], 'stove.png', 'Stove', False],
        [eco_elec[14], 'television.png', 'Television', False],
        [eco_elec[15], 'audio_system.png', 'Audio System', False],
    ]

    create_plot(df_list, plot_path + '/Building_2', 'ECO - Building 2 - ')

    eco_elec = read_dataset(path).buildings[3].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'laptop_computer.png', 'Laptop Computer', False],
        [eco_elec[5], 'freezer.png', 'Freezer', False],
        [eco_elec[6], 'coffee_maker.png', 'Coffee Maker', False],
        [eco_elec[7], 'computer.png', 'Computer', False],
        [eco_elec[8], 'fridge.png', 'Fridge', False],
        [eco_elec[9], 'kettle.png', 'Kettle', False],
        [eco_elec[10], 'HTPC.png', 'HTPC', False],
    ]

    create_plot(df_list, plot_path + '/Building_3', 'ECO - Building 3 - ')

    eco_elec = read_dataset(path).buildings[4].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'fridge.png', 'Fridge', False],
        [eco_elec[5], 'small_cooking_appliance.png', 'Small Cooking Appliance', False],
        [eco_elec[6], 'lamp.png', 'Lamp', False],
        [eco_elec[7], 'laptop_computer.png', 'Laptop Computer', False],
        [eco_elec[8], 'freezer.png', 'Freezer', False],
        [eco_elec[9], 'games_console.png', 'Games Console', False],
        [eco_elec[10], 'HTPC.png', 'HTPC', False],
        [eco_elec[11], 'microwave.png', 'Microwave', False],
    ]

    create_plot(df_list, plot_path + '/Building_4', 'ECO - Building 4 - ')

    eco_elec = read_dataset(path).buildings[5].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'laptop_computer.png', 'Laptop Computer', False],
        [eco_elec[5], 'coffee_maker.png', 'Coffee Maker', False],
        [eco_elec[6], 'garden_sprinkler.png', 'Garden Sprinkler', False],
        [eco_elec[7], 'microwave.png', 'Microwave', False],
        [eco_elec[8], 'fridge.png', 'Fridge', False],
        [eco_elec[9], 'HTPC.png', 'HTPC', False],
        [eco_elec[10], 'computer.png', 'Computer', False],
        [eco_elec[11], 'kettle.png', 'Kettle', False],
    ]

    create_plot(df_list, plot_path + '/Building_5', 'ECO - Building 5 - ')

    eco_elec = read_dataset(path).buildings[6].elec

    df_list = [
        [eco_elec, 'agregado.png', 'Agregado', False],
        [eco_elec[4], 'lamp.png', 'Lamp', False],
        [eco_elec[5], 'laptop_computer.png', 'Laptop Computer', False],
        [eco_elec[6], 'broadband_router.png', 'Broadband Router', False],
        [eco_elec[7], 'coffee_maker.png', 'Coffee Maker', False],
        [eco_elec[8], 'HTPC.png', 'HTPC', False],
        [eco_elec[9], 'fridge.png', 'Fridge', False],
        [eco_elec[10], 'kettle.png', 'Kettle', False],
    ]

    create_plot(df_list, plot_path + '/Building_6', 'ECO - Building 6 - ')

def lsd_data_plots(path, plot_path):
    lsd_elec = read_dataset(path).buildings[1].elec

    df_list = [
        [(lsd_elec.nested_metergroups()[0])[1], 'air_conditioner_1_24k.png', 'Air Conditioner 1 24k', False],
        [(lsd_elec.nested_metergroups()[0])[3], 'air_conditioner_2_24k.png', 'Air Conditioner 2 24k', False],
        [(lsd_elec.nested_metergroups()[0])[8], 'air_conditioner_3_24k.png', 'Air Conditioner 3 24k', False],
        [(lsd_elec.nested_metergroups()[0])[13], 'air_conditioner_4_24k.png', 'Air Conditioner 4 24k', False],
        [(lsd_elec.nested_metergroups()[0])[17], 'air_conditioner_5_24k.png', 'Air Conditioner 5 24k', False],
        [(lsd_elec.nested_metergroups()[0])[26], 'air_conditioner_6_24k.png', 'Air Conditioner 6 24k', False],
        [(lsd_elec.nested_metergroups()[0])[32], 'air_conditioner_7_24k.png', 'Air Conditioner 7 24k', False],
        [(lsd_elec.nested_metergroups()[1])[2], 'air_conditioner_1_18k.png', 'Air Conditioner 1 18k', False],
        [(lsd_elec.nested_metergroups()[1])[4], 'air_conditioner_2_18k.png', 'Air Conditioner 2 18k', False],
        [(lsd_elec.nested_metergroups()[1])[5], 'air_conditioner_3_18k.png', 'Air Conditioner 3 18k', False],
        [(lsd_elec.nested_metergroups()[1])[6], 'air_conditioner_4_18k.png', 'Air Conditioner 4 18k', False],
        [(lsd_elec.nested_metergroups()[1])[9], 'air_conditioner_5_18k.png', 'Air Conditioner 5 18k', False],
        [(lsd_elec.nested_metergroups()[1])[10], 'air_conditioner_6_18k.png', 'Air Conditioner 6 18k', False],
        [(lsd_elec.nested_metergroups()[1])[11], 'air_conditioner_7_18k.png', 'Air Conditioner 7 18k', False],
        [(lsd_elec.nested_metergroups()[1])[12], 'air_conditioner_8_18k.png', 'Air Conditioner 8 18k', False],
        [(lsd_elec.nested_metergroups()[1])[19], 'air_conditioner_9_18k.png', 'Air Conditioner 9 18k', False],
        [(lsd_elec.nested_metergroups()[1])[20], 'air_conditioner_10_18k.png', 'Air Conditioner 10 18k', False],
        [(lsd_elec.nested_metergroups()[1])[24], 'air_conditioner_11_18k.png', 'Air Conditioner 11 18k', False],
        [(lsd_elec.nested_metergroups()[1])[25], 'air_conditioner_12_18k.png', 'Air Conditioner 12 18k', False],
        [(lsd_elec.nested_metergroups()[1])[29], 'air_conditioner_13_18k.png', 'Air Conditioner 13 18k', False],
        [(lsd_elec.nested_metergroups()[2])[7], 'air_conditioner_1_36k.png', 'Air Conditioner 1 36k', False],
        [(lsd_elec.nested_metergroups()[2])[30], 'air_conditioner_2_36k.png', 'Air Conditioner 2 36k', False],
        [(lsd_elec.nested_metergroups()[2])[31], 'air_conditioner_3_36k.png', 'Air Conditioner 3 36k', False],
        [(lsd_elec.nested_metergroups()[3])[14], 'air_conditioner_1_12k.png', 'Air Conditioner 1 12k', False],
        [(lsd_elec.nested_metergroups()[3])[15], 'air_conditioner_2_12k.png', 'Air Conditioner 2 12k', False],
        [(lsd_elec.nested_metergroups()[3])[16], 'air_conditioner_3_12k.png', 'Air Conditioner 3 12k', False],
        [(lsd_elec.nested_metergroups()[3])[18], 'air_conditioner_4_12k.png', 'Air Conditioner 4 12k', False],
        [(lsd_elec.nested_metergroups()[3])[21], 'air_conditioner_5_12k.png', 'Air Conditioner 5 12k', False],
        [(lsd_elec.nested_metergroups()[3])[22], 'air_conditioner_6_12k.png', 'Air Conditioner 6 12k', False],
        [(lsd_elec.nested_metergroups()[3])[23], 'air_conditioner_7_12k.png', 'Air Conditioner 7 12k', False],
        [(lsd_elec.nested_metergroups()[3])[27], 'air_conditioner_8_12k.png', 'Air Conditioner 8 12k', False],
        [(lsd_elec.nested_metergroups()[3])[28], 'air_conditioner_9_12k.png', 'Air Conditioner 9 12k', False],
        [(lsd_elec.nested_metergroups()[4])[33], 'air_conditioner_1_9k.png', 'Air Conditioner 1 9k', False],
        [(lsd_elec.nested_metergroups()[4])[34], 'air_conditioner_2_9k.png', 'Air Conditioner 2 9k', False],
        [(lsd_elec.nested_metergroups()[4])[35], 'air_conditioner_3_9k.png', 'Air Conditioner 3 9k', False],
        [(lsd_elec.nested_metergroups()[4])[36], 'air_conditioner_4_9k.png', 'Air Conditioner 4 9k', False],
    ]

    create_plot(df_list, plot_path, 'LSD - ')

def redd_data_plots(path, plot_path):
    redd_elec = read_dataset(path).buildings[1].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec.nested_metergroups()[0], 'electric_oven.png', 'Electric Oven', True],
        [redd_elec[5], 'fridge.png', 'Fridge', False],
        [redd_elec[6], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[7], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[8], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
        [redd_elec[9], 'light_1.png', 'Light 1', False],
        [redd_elec.nested_metergroups()[1], 'washer_dryer.png', 'Washer Dryer', True],
        [redd_elec[11], 'microwave.png', 'Microwave', False],
        [redd_elec[12], 'bathroom_gfi.png', 'Bathroom Gfi', False],
        [redd_elec[13], 'electric_space_heater.png', 'Electric Space Heater', False],
        [redd_elec[14], 'electric_stove.png', 'Electric Stove', False],
        [redd_elec[15], 'kitchen_outlets_3.png', 'Kitchen Outlets 3', False],
        [redd_elec[16], 'kitchen_outlets_4.png', 'Kitchen Outlets 4', False],
        [redd_elec[17], 'light_2.png', 'Light 2', False],
        [redd_elec[18], 'light_3.png', 'Light 3', False],
    ]

    create_plot(df_list, plot_path + '/Building_1', 'REDD - Building 1 - ')

    redd_elec = read_dataset(path).buildings[2].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec[3], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[4], 'light_1.png', 'Light 1', False],
        [redd_elec[5], 'electric_oven.png', 'Electric Oven', False],
        [redd_elec[6], 'microwave.png', 'Microwave', False],
        [redd_elec[7], 'washer_dryer.png', 'Washer Dryer', False],
        [redd_elec[8], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
        [redd_elec[9], 'fridge.png', 'Fridge', False],
        [redd_elec[10], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[11], 'waste_disposal_unit.png', 'Waste Disposal Unit', False],
    ]

    create_plot(df_list, plot_path + '/Building_2', 'REDD - Building 2 - ')

    redd_elec = read_dataset(path).buildings[3].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec[3], 'outlets_unknown_1.png', 'Outlets Unknown 1', False],
        [redd_elec[4], 'outlets_unknown_2.png', 'Outlets Unknown 2', False],
        [redd_elec[5], 'light_1.png', 'Light 1', False],
        [redd_elec[6], 'ce_appliance.png', 'CE Appliance', False],
        [redd_elec[7], 'fridge.png', 'Fridge', False],
        [redd_elec[8], 'waste_disposal_unit.png', 'Waste Disposal Unit', False],
        [redd_elec[9], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[10], 'electric_furnace.png', 'Electric Furnace', False],
        [redd_elec[11], 'light_2.png', 'Light 2', False],
        [redd_elec[12], 'outlets_unknown_3.png', 'Outlets Unknown 3', False],
        [redd_elec.nested_metergroups()[0], 'washer_dryer.png', 'Washer Dryer', True],
        [redd_elec[15], 'light_3.png', 'Light 3', False],
        [redd_elec[16], 'microwave.png', 'Microwave', False],
        [redd_elec[17], 'light_4.png', 'Light 4', False],
        [redd_elec[18], 'smoke_alarms.png', 'Smoke Alarms', False],
        [redd_elec[19], 'light_5.png', 'Light 5', False],
        [redd_elec[20], 'bathroom_gfi.png', 'Bathroom Gfi', False],
        [redd_elec[21], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[22], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
    ]

    create_plot(df_list, plot_path + '/Building_3', 'REDD - Building 3 - ')

    redd_elec = read_dataset(path).buildings[4].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec[3], 'light_1.png', 'Light 1', False],
        [redd_elec[4], 'electric_furnace.png', 'Electric Furnace', False],
        [redd_elec[5], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[6], 'outlets_unknown_1.png', 'Outlets Unknown 1', False],
        [redd_elec[7], 'washer_dryer.png', 'Washer Dryer', False],
        [redd_elec[8], 'electric_stove.png', 'Electric Oven', False],
        [redd_elec.nested_metergroups()[0], 'air_conditioner_1.png', 'Air Conditioner 1', True],
        [redd_elec[11], 'miscellaeneous.png', 'Miscellaeneous', False],
        [redd_elec[12], 'smoke_alarms.png', 'Smoke Alarms', False],
        [redd_elec[13], 'light_2.png', 'Light 2', False],
        [redd_elec[14], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
        [redd_elec[15], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[16], 'bathroom_gfi_1.png', 'Bathroom Gfi 1', False],
        [redd_elec[17], 'bathroom_gfi_2.png', 'Bathroom Gfi 2', False],
        [redd_elec[18], 'light_3.png', 'Light 3', False],
        [redd_elec[19], 'light_4.png', 'Light 4', False],
        [redd_elec[20], 'air_conditioner_2.png', 'Air Conditioner 2', False],
    ]

    create_plot(df_list, plot_path + '/Building_4', 'REDD - Building 4 - ')

    redd_elec = read_dataset(path).buildings[5].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec[3], 'microwave.png', 'Microwave', False],
        [redd_elec[4], 'light_1.png', 'Light 1', False],
        [redd_elec[5], 'outlets_unknown_1.png', 'Outlets Unknown 1', False],
        [redd_elec[6], 'electric_furnace.png', 'Electric Furnace', False],
        [redd_elec[7], 'outlets_unknown_2.png', 'Outlets Unknown 2', False],
        [redd_elec.nested_metergroups()[0], 'washer_dryer.png', 'Washer Dryer', True],
        [redd_elec[10], 'subpanel_1.png', 'Subpanel 1', False],
        [redd_elec[11], 'subpanel_2.png', 'Subpanel 2', False],
        [redd_elec.nested_metergroups()[1], 'electric_space_heater.png', 'Electric Space Heater', True],
        [redd_elec[14], 'light_2.png', 'Light 2', False],
        [redd_elec[15], 'outlets_unknown_3.png', 'Outlets Unknown 3', False],
        [redd_elec[16], 'bathroom_gfi_1.png', 'Bathroom Gfi 1', False],
        [redd_elec[17], 'light_3.png', 'Light 3', False],
        [redd_elec[18], 'fridge.png', 'Fridge', False],
        [redd_elec[19], 'light_4.png', 'Light 4', False],
        [redd_elec[20], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[21], 'waste_disposal_unit.png', 'Waste Disposal Unit', False],
        [redd_elec[22], 'ce_appliance.png', 'CE Appliance', False],
        [redd_elec[23], 'light_5.png', 'Light 5', False],
        [redd_elec[24], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[25], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
        [redd_elec[26], 'outdoor_outlets_1.png', 'Outdoor Outlets 1', False],
    ]

    create_plot(df_list, plot_path + '/Building_5', 'REDD - Building 5 - ')

    redd_elec = read_dataset(path).buildings[6].elec

    df_list = [
        [redd_elec, 'agregado.png', 'Agregado', False],
        [redd_elec[3], 'kitchen_outlets_1.png', 'Kitchen Outlets 1', False],
        [redd_elec[4], 'washer_dryer.png', 'Washer Dryer', False],
        [redd_elec[5], 'electric_stove.png', 'Electric Stove', False],
        [redd_elec[6], 'ce_appliance.png', 'CE Appliance', False],
        [redd_elec[7], 'bathroom_gfi_1.png', 'Bathroom Gfi 1', False],
        [redd_elec[8], 'fridge.png', 'Fridge', False],
        [redd_elec[9], 'dish_washer.png', 'Dish Washer', False],
        [redd_elec[10], 'outlets_unknown_1.png', 'Outlets Unknown 1', False],
        [redd_elec[11], 'outlets_unknown_2.png', 'Outlets Unknown 2', False],
        [redd_elec[12], 'electric_space_heater.png', 'Electric Space Heater', False],
        [redd_elec[13], 'kitchen_outlets_2.png', 'Kitchen Outlets 2', False],
        [redd_elec[14], 'light_1.png', 'Light 1', False],
        [redd_elec[15], 'air_handling_unit.png', 'Air Handling Unit', False],
        [redd_elec.nested_metergroups()[0], 'air_conditioner.png', 'Air Conditioner', True],
    ]

    create_plot(df_list, plot_path + '/Building_6', 'REDD - Building 6 - ')


def main():
    # TODO: maintain the same y-axis scale for every split per appliance
    home_path = getenv("HOME")
    ampds_path = home_path + '/ProgrammingProjects/College/DatasetConverter/data/h5/AMPds2.h5'
    iawe_path = home_path + '/ProgrammingProjects/College/DatasetConverter/data/h5/iAWE.h5'
    eco_path = home_path + '/ProgrammingProjects/College/DatasetConverter/data/h5/ECO.h5'
    redd_path = home_path + '/ProgrammingProjects/College/DatasetConverter/data/h5/REDD.h5'
    lsd_path = home_path + '/temp/sinais.hdf5'
    plot_path = home_path + '/Documents/Plots'

    try:
        # AMPds Folders
        makedirs(home_path + '/Documents/Plots/AMPds/Ativa')
        makedirs(home_path + '/Documents/Plots/AMPds/Reativa')
        # iAWE Folders
        makedirs(home_path + '/Documents/Plots/iAWE/Ativa')
        makedirs(home_path + '/Documents/Plots/iAWE/Reativa')
        # ECO Folders
        makedirs(home_path + '/Documents/Plots/ECO/Building_1/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_1/Reativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_2/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_2/Reativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_3/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_3/Reativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_4/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_4/Reativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_5/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_5/Reativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_6/Ativa')
        makedirs(home_path + '/Documents/Plots/ECO/Building_6/Reativa')
        # REDD Folders
        makedirs(home_path + '/Documents/Plots/REDD/Building_1/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_1/Reativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_2/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_2/Reativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_3/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_3/Reativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_4/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_4/Reativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_5/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_5/Reativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_6/Ativa')
        makedirs(home_path + '/Documents/Plots/REDD/Building_6/Reativa')
        # LSD Folders
        makedirs(home_path + '/Documents/Plots/LSD/Ativa')
        makedirs(home_path + '/Documents/Plots/LSD/Reativa')
    except FileExistsError:
        pass

    ampds_data_plots(ampds_path, plot_path + '/AMPds')
    iawe_data_plots(iawe_path, plot_path + '/iAWE')
    eco_data_plots(eco_path, plot_path + '/ECO')
    lsd_data_plots(lsd_path, plot_path + '/LSD')
    redd_data_plots(redd_path, plot_path + '/REDD')

if __name__ == '__main__':
    main()
