import json
from os import getenv, makedirs

import matplotlib.pyplot as plt


def populate_dict(path, data):
    for epoch in ['1', '5', '15', '30']:
        for appliance in data.keys():
            json_file = read_json(path + '/' + epoch + '/' + appliance + '.json')
            data[appliance].append(json_file['accuracy'])

    return data


def read_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


def plot_line_graph(dict, title, path):
    plt.subplots(figsize=(20, 10))
    for key in dict.keys():
        plt.xticks(range(len(dict[key])), [1, 5, 15, 30])
        plt.grid(True)
        plt.ylabel("Acurácia")
        plt.xlabel("Epochs")
        plt.title(title)
        plt.plot(range(len(dict[key])), dict[key], label=key)
        plt.legend()
    plt.savefig(path, format='png', dpi=300)
    plt.clf()


def main():
    appliances = {
        'hair_dryer', 'wet_appliance', 'computer', 'coffee_maker', 'fridge', 'sockets',
        'unknown', 'washing_machine', 'freezer', 'clothes_iron', 'television', 'heat_pump',
        'air_conditioner', 'electric_oven', 'kettle', 'light'
    }

    home_path = getenv("HOME")
    ampds_path = home_path + '/Documents/Results/AMPds'
    eco_path = home_path + '/Documents/Results/eco'
    iawe_path = home_path + '/Documents/Results/iawe'
    plot_path = home_path + '/Documents/Plots'

    ampds_data = {
        'light': [], 'sockets': [], 'unknown': [], 'fridge': [],
        'heat_pump': [], 'electric_oven': [], 'television': []
    }

    # coffee_maker, kettle - Problem with data
    eco_building1_data = {
        'computer': [], 'freezer': [], 'fridge': [], 'hair_dryer': [],
        'washing_machine': []
    }

    # fridge - Problem with data
    iawe_data = {
        'wet_appliance': [], 'air_conditioner': [], 'computer': [], 'clothes_iron': [],
        'unknown': [], 'television': [], 'washing_machine': []
    }

    ampds_data = populate_dict(ampds_path, ampds_data)
    eco_building1_data = populate_dict(eco_path + '/building1', eco_building1_data)
    iawe_data = populate_dict(iawe_path, iawe_data)

    try:
        makedirs(home_path + '/Documents/Plots')
    except FileExistsError:
        pass

    plot_line_graph(ampds_data, 'AMPds Dataset', plot_path + '/ampds_line_plot.png')
    plot_line_graph(eco_building1_data, 'ECO Dataset - Building 1', plot_path + '/eco_building1_line_plot.png')
    plot_line_graph(iawe_data, 'iAWE Dataset', plot_path + '/iawe_line_plot.png')


if __name__ == '__main__':
    main()
