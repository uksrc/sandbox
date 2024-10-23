# Correct tests can/will be written here,
# Just need to get to learning to use pytest!



import pytest
import casatools
import eMERLIN_metadata_extract 
import sys

msmd = casatools.msmetadata()
emd = eMERLIN_metadata_extract

data_path = "/Users/user/dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"
#data_path = sys.argv[1]
print("Path:", data_path)

# Test Observing frequency, channel resolution, number of channels
# Expected: 4 obs freq: 
#	    Channel width/res: 1000 
#	    Channels: 128000
#
# At the minute, this isn't fully giving expected results.
# To do: read more info into a better data structure with this nspw call.
# To do: convert units to wavelength from frequency for standard. 
    
#freq_ini, freq_end, chan_res, nchan = eMERLIN_metadata_extract.get_obsfreq(data_path)
#print("Initial freq:",freq_ini)
#print("End freq:",freq_end)
#print("Channel width:",chan_res)
#print("Num Chans:",nchan)

# Test energy_bounds, converts to wavelength as per the data model requirements.
# Gets upper and lower energy bounds for this observation.
# Test energy bounds Hz to m
#energy_bounds_up, energy_bounds_low = emd.energy_bounds(data_path)
#print('energy range(m):',energy_bounds_low,'-',energy_bounds_up)


# Test using table.getcol to extract the project id, obsid.  also could extract this from file path or file name.  

#project_id = eMERLIN_metadata_extract.get_proj_id(data_path)
#print("Project ID ",project_id)

# Test and print getting source names

# Expected: 0319+4130, 1252+5634, 1302+5748, 1331+3030, 1407+2827 
#sources = eMERLIN_metadata_extract.find_mssources(data_path)
#print(sources)

# Figure out which source is the primary target, and which are cals.

#source_name, source_type, source_ref_dir = emd.find_target(data_path)
#print(source_name)
#print(source_type)
#print(source_ref_dir)

# ADD ME
# Test start/end times of observation
#start_time, end_time = emd.get_obstime(data_path)
#print(start_time)
#print(end_time)

rel_date = emd.get_release_date(data_path)
print(rel_date)

# Get antenna names.  Expect Mk2, Pi, Da, Kn, De, Cm.

#antlist = eMERLIN_metadata_extract.get_antennas(data_path)
#print(antlist)

#ant_geo = emd.get_ref_ant(data_path, antlist)
#print(ant_geo)

# Get eMERLIN bp name.  Expect Band CC
# To do: Test Null result, cannot fetch band region.
 
#band_name = eMERLIN_metadata_extract.get_bandpass(data_path)
#print(band_name)

temp_pol_state, dim = emd.get_polarization(data_path)
print(temp_pol_state)
print(dim)

#mode, cal = emd.state(data_path)
#print(mode, cal)

#hist_row = emd.testing_tables(data_path)
#print(hist_row)

#print("Test consolidated structure:")
casa_elements_dict = emd.msmd_collect(data_path)
print(casa_elements_dict)
#all_scans = emd.get_scan_sum(data_path)
#print(len(all_scans))
