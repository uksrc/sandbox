
import casatools
import measurement_sets
import sys

msmd = casatools.msmetadata()

#data_path = "dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"
data_path = sys.argv[1]
print("Path:", data_path)

# Populate key summary to test function

subset_keys_vals = measurement_sets.summary_metadata(data_path)

for each_key in subset_keys_vals:
	print(each_key)

# Check against what is contained in actual dictionary, because for loop is only printing the headers it seems, not sure how to extract values at the minute, so no way to parse them.
# print(subset_keys_vals)
