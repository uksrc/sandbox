import casatools

msmd = casatools.msmetadata()
ms = casatools.ms()
tb = casatools.table()



ms_path = "/home/h14471mj/e-merlin/casa6_docker/prod/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"


# initial header extraction funtion, formatting/cleaning not included for now
def get_local_headers_from_ms(ms_file):
    '''
    Get list of ms headers from measurement set
    :param ms_file:
    :return: list of headers
    '''
    tb.open(ms_file)
    colnames = tb.colnames()
    tb.close()
    return colnames

def get_headers_from_ms_kvp(ms_file):
    '''
    Get key:value pairs in dictionary for headers in a measurement set.
    :param ms_file: measurement set name
    :return: Dictionary of key-value pairs header names: values
    '''
    col_names = get_local_headers_from_ms(ms_file)
    ms.open(ms_file)
    query = ms.getdata(col_names)
    ms.selectinit(reset=True)
    ms.close()
    return query


