# This module extracts metadata from eMERLIN measurement sets to be 
# ingested into an eMERLIN metadata database, and a CAOM database.  
#
# To do: Once we know what a unit of ingest will look like, reduce 
# the msmetadata.open calls and extract metadata into structures that
# are most meaningful for the CAOM tables.  

from casatools import msmetadata, table
import numpy

tb = casatools.table()
msmd = casatools.msmetadata()

#ms_path = "dataRedution/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"

def get_proj_id(ms_file):
    # Get the 'project' code which should be what we call obsid?  Check with Paul?
    tb.open(ms_file+'/OBSERVATION')
    project_id = tb.getcol('PROJECT')
    tb.close()
    return project_id[0]

#def test_get_proj_id():
#    assert get_proj_id(dataRedution/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms) == 'TS8005' 


def get_release_date(ms_file):
    # Try to get public data date from metadata.
    # Cannot make sense of this yet... not julian but not sure what it is!
    tb.open(ms_file+'/OBSERVATION')
    release_date = tb.getcol('RELEASE_DATE')
    tb.close()
    return release_date[0]

def testing_tables(ms_file):
    # Get description of cols/headers, hopefully.
    # 
    tb.open(ms_file+'/OBSERVATION')
    table_dict = tb.getdesc()
    tb.close()
    return table_dict

def find_mssources(ms_file):
    # Get list of sources from measurement set
    # To do: discern target and calibrators for CAOM Observation.targetName
    msmd.open(ms_file)
    mssources = ','.join(numpy.sort(msmd.fieldnames()))
    #mssources = msmd.fieldnames()
    msmd.done()
    return mssources

def find_target(ms_file):
    # Try to find which source has which purpose.
    tb.open(ms_file+'/FIELD')
    source_type = tb.getcol('NAME')
    tb.close()
    return source_type

def get_antennas(ms_file):
    # Returns Antenna names list included in interferometer for this obs
    # To do: place each in CAOM Observation.telescopeKeyword 
    msmd.open(ms_file)
    antennas = msmd.antennanames()
    msmd.close()
    # nice_order = ['Lo', 'Mk2', 'Pi', 'Da', 'Kn', 'De', 'Cm']
    # antennas = [a for a in nice_order if a in antennas]
    # logger.debug('Antennas in MS {0}: {1}'.format(msfile, antennas))
    return antennas


# At the minute, this isn't fully giving expected results.
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
# Updated to return CAOM format and receptor count instead of eMERLIN weblog format..  
    tb.open(ms_file+'/FEED')
    polarization = tb.getcol('POLARIZATION_TYPE')
    pol_dim = tb.getcol('NUM_RECEPTORS')[0]
    tb.close()
    return "PolarizationState."+''.join(polarization[:,0]), pol_dim

