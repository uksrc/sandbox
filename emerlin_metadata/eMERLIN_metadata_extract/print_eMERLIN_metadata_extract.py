# Tests eMERLIN_metadata_extract functions.


import pytest
import casatools
from eMERLIN_metadata_extract import * 
import sys

msmd = casatools.msmetadata()
emd = eMERLIN_metadata_extract

data_path = "dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"
#data_path = sys.argv[1]
#print("Path:", data_path)

# Test Observing frequency, channel resolution, number of channels
# Expected: 4 obs freq: 
#	    Channel width/res: 1000 
#	    Channels: 128000
#
# To do: read more info into a better data structure with this nspw call.
    
def test_emd.get_obsfreq()
    freq_ini, freq_end, chan_res, nchan = eMERLIN_metadata_extract.get_obsfreq(data_path)
    assert freq_ini, freq_end, chan_res, nchan == 4.8165, 5.3275, 0.001, 128

#print("Initial freq:",freq_ini)
#print("End freq:",freq_end)
#print("Channel width:",chan_res)
#print("Num Chans:",nchan)

# Test energy_bounds, converts to wavelength as per the data model requirements.
# Gets upper and lower energy bounds for this observation.
# Test energy bounds Hz to m
energy_bounds_up, energy_bounds_low = emd.energy_bounds(data_path)
print('energy range(m):',energy_bounds_low,'-',energy_bounds_up)


# Test using table.getcol to extract the project id, obsid.  also could extract this from file path or file name.  

project_id = eMERLIN_metadata_extract.get_proj_id(data_path)
print("Project ID ",project_id)

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

temp_pol_state, dim = emd.get_polarization(data_path)
print(temp_pol_state)
print(dim)
