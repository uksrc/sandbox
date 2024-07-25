import casatools
from astropy.io import fits
import numpy as np

msmd = casatools.msmetadata()

ms_path = "/home/h14471mj/e-merlin/casa6_docker/prod/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"


def summary_metadata(ms_path):
    '''
    Extract summery of metadata for entire measurement set
    :param ms_file: input measurement set location
    :return: Dictionary of metadata descrbing:['begin time', 'data descriptions', 'end time', 'fields', 'nrows',
     'polarizations', 'spectral windows']
    '''

    msmd.open(ms_path)
    sum_dict = msmd.summary()
    sum_keys = sum_dict.keys()
    msmd.done()

    del_for_now = [key for key in sum_keys if 'observationID' in key]
    for key in del_for_now:
        del sum_dict[key]

    # removing field specific metadata for now, include later
    # Current test dataset for observationID data has structure ['observationID=0']['arrayID=0']['scan=1']['fieldID=3'],
    # followed by 'antennas', 'begin time', 'data description IDs', 'end time', 'nrows', 'state IDs', and ~600 fields,
    # each with ['data description IDs', 'nrows', 'time']
    return sum_dict


def get_scan_sum(ms_file):
    '''
    Returns metadata per scan for a measurement set
    :param ms_file: Input directory for measurement set
    :return: casa dictionary of metadata
    '''
    ms.open(ms_file)
    scan_sum = ms.getscansummary()
    ms.close()
    return scan_sum


def convert_casa_output_to_fits(ms_dict):
    '''
    Converts the casa dictionary to the fits header class need for the caom code
    :param ms_dict: converted dictionary (currently configure only for get_scan_sum)
    :return: fits Header object to be inserted into the caom code
    '''
    hdu_list = []
    for key, item in ms_dict.items():
        for key_2, item_2 in item.items():
            ms_header = fits.Header()
            for head_key, head_value in item_2.items():
                try:
                    ms_header[head_key] = head_value
                except ValueError:
                    ms_header[head_key] = str(head_value)
                hdu_list.append(ms_header)

    return hdu_list


ms_dict = get_scan_sum(ms_path)
ms_header = convert_casa_output_to_fits(ms_dict)
