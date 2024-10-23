# This module extracts metadata from eMERLIN measurement sets to be 
# ingested into an eMERLIN metadata database, and a CAOM database.  
#
# To do: Once we know what a unit of ingest will look like, reduce 
# the msmetadata.open calls and extract metadata into structures that
# are most meaningful for the CAOM tables.  

import casatools
import numpy
import datetime

tb = casatools.table()
msmd = casatools.msmetadata()
ms = casatools.ms()

#ms_path = "dataRedution/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"

# Try to reduce to one open and close for each casatools operation.
def msmd_collect(ms_file):
    """
    Consolidate opening measurement set to one function
    :param ms_file: Input measurement set
    :returns msmd_elements: data structure dictionary of relevant metadata
    """

    msmd.open(ms_file)
    nspw = msmd.nspw()
    msmd_elements = {
        'mssources': msmd.fieldnames(),
        'tel_name': msmd.observatorynames(),
        'antennas': msmd.antennanames(),
        'wl_upper': msmd.chanfreqs(0)[0],
        'wl_lower': msmd.chanfreqs(nspw-1)[-1],
        'chan_width': msmd.chanwidths(0)[0],
        'nchan': len(msmd.chanwidths(0)),
    }

    nice_order = ['Lo', 'Mk2', 'Pi', 'Da', 'Kn', 'De', 'Cm']
    refant = [a for a in nice_order if a in msmd_elements['antennas']]
    geo = msmd.antennaposition(refant[0])
    msmd.close()

    # Dictionary of changes
    elements_convert = {
        'wl_upper': freq2wl(msmd_elements['wl_upper']),
        'wl_lower': freq2wl(msmd_elements['wl_lower']),
        'chan_width': msmd_elements['chan_width']/1e9,
        'bp_name': emerlin_band(msmd_elements['wl_upper']),
        'geoloc_x': geo["m0"]["value"],
        'geoloc_y': geo["m1"]["value"],
        'geoloc_z': geo["m2"]["value"]
    }

    # Update dictionary with converted values and additions.
    msmd_elements.update(elements_convert)

    return msmd_elements

def ms_other_collect(ms_file):
    """
    Consolidate non-msmd-type opens to a second dictionary?
    param ms_file: Input measurement set
    returns ms_other_elements: dictionary of non-msmd-retrievable elements \
                               which need various table/col combinations. 
    """

    ms_other_elements = {
        'data_release': get_release_date(ms_file),
        'obs_start_time': get_obstime(ms_file)[0],
        'obs_stop_time': get_obstime(ms_file)[1],
        'polar_dim': get_polar(ms_file)[2]
    }

    return ms_other_elements

def emerlin_band(freq):
    """
    Determine eMERLIN band name from frequency
    :param freq: Frequency in Hz
    :return band_name: string
    """
    freq = freq/1e9
    if (freq > 1.2) and (freq < 1.7):
        band = 'L'
    elif (freq > 4) and (freq < 8):
        band = 'C'
    elif (freq > 17) and (freq < 26):
        band = 'K'
    else:
        print('Cannot determine band from frequency')
        band = 'Null'
    return band

def mjdtodate(mjd):
    # Stolen from eMCP_functions.py for date conversion.
    origin = datetime.datetime(1858,11,17)
    date = origin + datetime.timedelta(mjd)
    return date

# ADD THIS
def get_obstime(ms_file):
    # returns datetime object of first and last times in obs_id 0
    # DONT convert to datetime! caom wants DOUBLE for datatype. 
    ms.open(ms_file)
    t = ms.getdata('TIME')['time']
    t_ini = numpy.min(t)
    t_end = numpy.max(t)
    #t_ini = mjdtodate(numpy.min(t)/60./60./24)
    #t_end = mjdtodate(numpy.max(t)/60./60./24)
    ms.close()
    return t_ini, t_end

def get_proj_id(ms_file):
    # Get the 'project' code which should be what we call obsid?  Check with Paul?
    tb.open(ms_file+'/OBSERVATION')
    project_id = tb.getcol('PROJECT')
    tb.close()
    return project_id[0]


# ADD THIS
def get_release_date(ms_file):
    # in mjd seconds... which is what caom wants.  
    # Commented out conversion to 'normal' datetime. 
    tb.open(ms_file+'/OBSERVATION')
    rel_date = tb.getcol('RELEASE_DATE')
    # rel_date = mjdtodate(rel_date[0]/60./60./24)
    tb.close()
    return rel_date

def testing_tables(ms_file):
    # Get description of cols/headers, hopefully.
    # 
    tb.open(ms_file+'/HISTORY')
    table_dict = tb.row('MESSAGE')[1150:1200]
    tb.close()
    return table_dict

def state(ms_file):
    # Check obs_mode result in ms.
    tb.open(ms_file+'/STATE')
    obs_mode = tb.getcol('OBS_MODE')
    cal_info = tb.getcol('CAL')
    tb.close()
    return obs_mode, cal_info

def find_mssources(ms_file):
    # Get list of sources from measurement set
    # To do: discern target and calibrators for CAOM Observation.targetName
    msmd.open(ms_file)
    mssources = ','.join(numpy.sort(msmd.fieldnames()))
    #mssources = msmd.fieldnames()
    msmd.done()
    return mssources

def get_hist(ms_file):
    tb.open(ms_file+'/HISTORY')
    hist = tb.getcol('MESSAGE')
    tb.close()

def find_target(ms_file):
    # Try to find which source has which purpose. Source table, source ID don't exist. Ref_dir and phase_dir are same.
    tb.open(ms_file+'/FIELD')
    source_name = tb.getcol('NAME')
    source_type = tb.getcol('CODE')
    source_ph_dir = tb.getcol('REFERENCE_DIR')
    tb.close()
    return source_name, source_type, source_ph_dir 

def get_antennas(ms_file):
    # Returns Antenna names list included in interferometer for this obs
    # To do: place each in CAOM Observation.telescopeKeyword 
    msmd.open(ms_file)
    antennas = msmd.antennanames()
    msmd.close()
    #nice_order = ['Lo', 'Mk2', 'Pi', 'Da', 'Kn', 'De', 'Cm']
    #antennas = [a for a in nice_order if a in antennas]
    return antennas

def ref_ant_geo(ms_file, antennas):
    '''
    Based on correlator reference order, choose geoloc of first antenna \
    in the eMERLIN 'nice_order' list. 
    :params: measurement set, list of antennas in array
    :return: geolocation for first antenna in array.
    ''' 
    nice_order = ['Lo', 'Mk2', 'Pi', 'Da', 'Kn', 'De', 'Cm']
    antennas = [a for a in nice_order if a in antennas]
    msmd.open(ms_file)
    geo = msmd.antennaposition(antennas[0])
    msmd.close()
    geoloc_x = geo["m0"]["value"]
    geoloc_y = geo["m1"]["value"]
    geoloc_z = geo["m2"]["value"]
    return geoloc_x, geoloc_y, geoloc_z 

# To do: read more info into a better data structure with this nspw call.

def get_obsfreq(ms_file):
    # Returns freq of first channel, end chan, channel resolution
    # and number of channels (first spw) in GHz
    msmd.open(ms_file)
    nspw = msmd.nspw()
    freq_ini = msmd.chanfreqs(0)[0]/1e9
    freq_end = msmd.chanfreqs(nspw-1)[-1]/1e9
    chan_res = msmd.chanwidths(0)[0]/1e9
    nchan = len(msmd.chanwidths(0))
    msmd.done()
    return freq_ini, freq_end, chan_res, nchan

def freq2wl(freq):
    # Convert frequency (Hz) to wavelength (m)
    sol = 299792458
    wl = sol/freq
    return wl

def energy_bounds(ms_file):
    # Return energy bounds in wavelength (m)
    msmd.open(ms_file)
    nspw = msmd.nspw()
    freq_ini = msmd.chanfreqs(0)[0]
    freq_end = msmd.chanfreqs(nspw-1)[-1]
    wl_upper = freq2wl(freq_ini) 
    wl_lower = freq2wl(freq_end)
    return wl_upper, wl_lower 

def get_bandpass(ms_file):
    # Returns eMERLIN name for bandpass CAOM Energy.bandpassName
    # To do: Combine with get_obsfreq for one open on nspw?
    msmd.open(ms_file)
    freq = msmd.chanfreqs(0)[0]/1e9
    msmd.done()
    band = ''
    if (freq > 1.2) and (freq < 1.7):
        band = 'L'
    elif (freq > 4) and (freq < 8):
        band = 'C'
    elif (freq > 17) and (freq < 26):
        band = 'K'
    else:
        print('Cannot determine band from frequency')
        band = 'Null' 
    return band
   
def get_polarization(ms_file):
# Duplicated from eMERLIN_CASA_pipeline/functions/eMCP_functions.py
# Polarization Table is empty, if I recall correctly.
# Updated to return CAOM format and receptor count instead of eMERLIN weblog format..  
    tb.open(ms_file+'/FEED')
    polarization = tb.getcol('POLARIZATION_TYPE')
    pol_dim = tb.getcol('NUM_RECEPTORS')[0:]
    tb.close()
    return "PolarizationState."+''.join(polarization[:,0]), pol_dim

