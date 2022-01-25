# WaveNILM Converter

WaveNILM Converter is a tool developed to help convert NILM datasets for use with WaveNILM. Files need to be in H5 format according to NILMTK.

## Dependencies

To install WaveNILM Converter dependencies, run the following steps:

```
pip install -r requirements.txt
```

## Parameters

WaveNILM Converter for now supports the following arguments:

| Name | Description |
| --- | --- |
| `-a`/`--ampds` | Enables conversion for AMPDS dataset. **(Optional)** |
| `-i`/`--iawe` | Enables conversion for iAWE dataset. **(Optional)** |
| `-e [building_number]`/`--eco [building_number]` | Enables conversion for ECO dataset. Needs to specify buildings. **(Optional)** |
| `-r [building_number]`/`--redd [building_number]` | Enables conversion for REDD dataset. Needs to specify buildings. **(Optional)** |
| `-d [file_path]`/`--dat [file_path]` | Path to save DAT files. **(Optional)** |
| `-m`/`--multiple_load` | Enables multiple load conversion for all datasets. It generates a dat file with load from the 5 appliances with the highest electricity consumption on that building. **(Optional)** |
| `-s`/`--single_load` | Enables single load conversion for all datasets. Each appliance is saved to dat file with both Active and Reactive Power. If Reactive Power is not available, only Active Power is used. **(Optional)** |

## Examples

Below you can find some examples of how to run the tool.

#### Convert AMPds Dataset with both Multiple and Single Loads

```
python3 main.py --ampds --dat 'path/to/file' --multiple_load --single_load
```

#### Convert Building 1 from REDD Datasets for Single Load only

```
python3 main.py --redd 1 --dat 'path/to/file' --single_load
```
