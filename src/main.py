from os import getcwd, path
from converters.ampds.converter import AmpdsConverter
from converters.eco.converter import EcoConverter

def main():
    eco = EcoConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4])

    #ampds = AmpdsConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4])

    eco.convert_df()
    #ampds.convert_df()

    exit(0)

if __name__ == '__main__':
    main()