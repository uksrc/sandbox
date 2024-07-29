# This module extracts metadata from eMERLIN measurement sets to be 
# ingested into an eMERLIN metadata database, and a CAOM database.  
#
# To do: Once we know what a unit of ingest will look like, reduce 
# the msmetadata.open calls and extract metadata into structures that
# are most meaningful for the CAOM tables.  

import casatools
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

def find_mssources(ms_file):
    # Get list of sources from measurement set
    # To do: discern target and calibrators for CAOM Observation.targetName
    msmd.open(ms_file)
    mssources = ','.join(numpy.sort(msmd.fieldnames()))
    #mssources = msmd.fieldnames()
    msmd.done()
    # logger.debug('Sources in MS {0}: {1}'.format(msfile, mssources))
    return mssources

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
# To do: convert units to wavelength from frequency for standard.

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
    
