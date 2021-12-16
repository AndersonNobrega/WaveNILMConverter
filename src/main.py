import argparse
import logging
from os import getcwd, path

from converters.ampds.converter import AmpdsConverter
from converters.eco.converter import EcoConverter
from converters.iawe.converter import IaweConverter
from converters.redd.converter import ReddConverter


def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description='Converts NILMTK h5 files to dat for use with WaveNILM.')

    parser.add_argument('-a', '--ampds', action='store_true', help='Enables conversion for AMPDS dataset.')
    parser.add_argument('-e', '--eco', nargs='+', type=int,
                        help='Enables conversion for ECO dataset. Needs to specify buildings.')
    parser.add_argument('-i', '--iawe', action='store_true', help='Enables conversion for iAWE dataset.')
    parser.add_argument('-r', '--redd', nargs='+', type=int,
                        help='Enables conversion for REDD dataset. Needs to specify buildings.')
    parser.add_argument('-d', '--dat', type=str, help='Path to save DAT files.')
    parser.add_argument('-m', '--multiple_load', action='store_true',
                        help='Enables multiple load conversion for all datasets.')
    parser.add_argument('-s', '--single_load', action='store_true',
                        help='Enables single load conversion for all datasets.')

    args = vars(parser.parse_args())

    base_path = path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4]

    dat_path = base_path + '/data/dat/'

    multiple_load = False
    single_load = False

    if args['multiple_load']:
        multiple_load = True
    if args['single_load']:
        single_load = True

    if args['ampds']:
        logging.info('Starting AMPds dataset conversion.')
        if args['dat'] is None:
            AmpdsConverter(dir_path=base_path, dat_path=dat_path + 'ampds', single_loads=single_load,
                           multiple_loads=multiple_load).convert_df()
        else:
            AmpdsConverter(dir_path=base_path, dat_path=args['dat'], single_loads=single_load,
                           multiple_loads=multiple_load).convert_df()
        logging.info('AMPds dataset conversion completed.')

    if args['iawe']:
        logging.info('Starting iAWE dataset conversion.')
        if args['dat'] is None:
            IaweConverter(dir_path=base_path, dat_path=dat_path + 'iawe', single_loads=single_load,
                          multiple_loads=multiple_load).convert_df()
        else:
            IaweConverter(dir_path=base_path, dat_path=args['dat'], single_loads=single_load,
                          multiple_loads=multiple_load).convert_df()
        logging.info('iAWE dataset conversion completed.')

    if args['eco']:
        logging.info('Starting ECO dataset conversion.')
        if args['dat'] is None:
            EcoConverter(dir_path=base_path, dat_path=dat_path + 'eco', single_loads=single_load,
                         multiple_loads=multiple_load).convert_df(args['eco'])
        else:
            EcoConverter(dir_path=base_path, dat_path=args['dat'], single_loads=single_load,
                         multiple_loads=multiple_load).convert_df(args['eco'])
        logging.info('ECO dataset conversion completed.')

    if args['redd']:
        logging.info('Starting REDD dataset conversion.')
        if args['dat'] is None:
            ReddConverter(dir_path=base_path, dat_path=dat_path + 'redd', single_loads=single_load,
                          multiple_loads=multiple_load).convert_df(args['redd'])
        else:
            ReddConverter(dir_path=base_path, dat_path=args['dat'], single_loads=single_load,
                          multiple_loads=multiple_load).convert_df(args['redd'])
        logging.info('REDD dataset conversion completed.')

    exit(0)


if __name__ == '__main__':
    main()
