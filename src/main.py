from converters.ampds.converter import AmpdsConverter
from converters.eco.converter import EcoConverter
from converters.iawe.converter import IaweConverter
from os import getcwd, path

import argparse
import logging

def main():
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False, description='Converts NILMTK h5 files to dat for use with WaveNILM.')

    parser.add_argument('-a', '--ampds', action='store_true', help='Enables conversion for AMPDS dataset.')
    parser.add_argument('-e', '--eco', nargs='+', type=int, help='Enables conversion for ECO dataset. Needs to specify buildings.')
    parser.add_argument('-i', '--iawe', action='store_true', help='Enables conversion for iAWE dataset.')
    args = vars(parser.parse_args())
    
    if args['ampds']:
        logging.info('Starting AMPDS dataset conversion.')
        AmpdsConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4]).convert_df()
        logging.info('AMPDS dataset conversion completed.')

    if args['iawe']:
        logging.info('Starting AMPDS dataset conversion.')
        IaweConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4]).convert_df()
        logging.info('AMPDS dataset conversion completed.')
    
    if args['eco']:
        logging.info('Starting ECO dataset conversion.')
        EcoConverter(dir_path=path.realpath(path.join(getcwd(), path.dirname(__file__)))[:-4]).convert_df(args['eco'])
        logging.info('ECO dataset conversion completed.')

    exit(0)

if __name__ == '__main__':
    try:
        main()
    except MemoryError:
        logging.error('Memory Exception')
        exit(1)