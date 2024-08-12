# Tests eMERLIN_metadata_extract functions.


import pytest
from eMERLIN_metadata_extract.eMERLIN_metadata_extract import *
data_path = "/Users/user/dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"
#data_path = sys.argv[1]
#print("Path:", data_path)

    
#def test_emd.get_obsfreq():
#    freq_ini, freq_end, chan_res, nchan = eMERLIN_metadata_extract.get_obsfreq(data_path)
#    assert freq_ini, freq_end, chan_res, nchan == 4.8165, 5.3275, 0.001, 128


# Test energy_bounds, converts to wavelength as per the data model requirements.
# Gets upper and lower energy bounds for this observation.
# Test energy bounds Hz to m
# energy_bounds_up, energy_bounds_low = emd.energy_bounds(data_path)
# print('energy range(m):',energy_bounds_low,'-',energy_bounds_up)


# Test using table.getcol to extract the project id, obsid.  also could extract this from file path or file name.  

def test_emd_get_proj_id():
    project_id = eMERLIN_metadata_extract.get_proj_id(data_path)
    assert project_id == 'TS8004'

#print("Project ID ",project_id)

# Test and print getting source names

# Expected: 0319+4130, 1252+5634, 1302+5748, 1331+3030, 1407+2827 
#sources = eMERLIN_metadata_extract.find_mssources(data_path)
#print(sources)

# Get antenna names.  Expect Mk2, Kn, De, Pi, Da, Cm.

#antlist = eMERLIN_metadata_extract.get_antennas(data_path)
#print(antlist)

# Get eMERLIN bp name.  Expect Band CC
# To do: Test Null result, cannot fetch band region.
 
#band_name = eMERLIN_metadata_extract.get_bandpass(data_path)
#print(band_name)

#temp_pol_state, dim = emd.get_polarization(data_path)
#print(temp_pol_state)
#print(dim)
