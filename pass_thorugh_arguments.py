import sys
import measurement_sets

file_name = sys.argv[1]
metadata = measurement_sets.summary_metadata(file_name)
print(metadata)