import casatools

msmd = casatools.msmetadata()

ms_path = "/home/h14471mj/e-merlin/casa6_docker/prod/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"


def summary_metadata(ms_file):
    '''
    Extract summery of metadata for entire measurement set
    :param ms_file: input measurement set location
    :return: Dictionary of metadata descrbing:['begin time', 'data descriptions', 'end time', 'fields', 'nrows',
     'polarizations', 'spectral windows']
    '''

    msmd.open(ms_file)
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


