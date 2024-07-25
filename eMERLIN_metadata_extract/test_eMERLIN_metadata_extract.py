# Correct tests can/will be written here,
# Just need to get to learning to use pytest!



import pytest
import casatools
import eMERLIN_metadata_extract 
import sys

msmd = casatools.msmetadata()
emd = eMERLIN_metadata_extract

#data_path = "dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"
data_path = sys.argv[1]
print("Path:", data_path)

# Test Observing frequency, channel resolution, number of channels
# Expected: 4 obs freq: 
#	    Channel width/res: 1000 
#	    Channels: 128000
#
# At the minute, this isn't fully giving expected results.
# To do: read more info into a better data structure with this nspw call.
# To do: convert units to wavelength from frequency for standard. 
    
freq_ini, freq_end, chan_res, nchan = eMERLIN_metadata_extract.get_obsfreq(data_path)
print("Initial freq:",freq_ini)
print("End freq:",freq_end)
print("Channel width:",chan_res)
print("Num Chans:",nchan)



# Test and print getting source names

# Expected: 0319+4130, 1252+5634, 1302+5748, 1331+3030, 1407+2827 
sources = eMERLIN_metadata_extract.find_mssources(data_path)
print(sources)

# Get antenna names.  Expect Mk2, Kn, De, Pi, Da, Cm.

antlist = eMERLIN_metadata_extract.get_antennas(data_path)
print(antlist)

# Get eMERLIN bp name.  Expect Band CC
# To do: Test Null result, cannot fetch band region.
 
band_name = eMERLIN_metadata_extract.get_bandpass(data_path)
print(band_name)
