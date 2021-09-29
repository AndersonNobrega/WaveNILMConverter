from os import getcwd, path
from converters.ampds.converter import AmpdsConverter

def main():
    ampds = AmpdsConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4])

    ampds.convert_df()

    exit(0)

if __name__ == '__main__':
    main()