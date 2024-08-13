# Check for empty measurement set tables so we know to skip them.
# Return tables that have rows?

import sys
import os
import glob
import casatools
import numpy

tb = casatools.table()
msmd = casatools.msmetadata()

ms_dir = sys.argv[1]
#ms_dir = "/Users/user/dataReduction/TS8004_C_001_20190801/TS8004_C_001_20190801_avg.ms"

ms_dirs = glob.glob(ms_dir+"/*")

#print("Number of tables in ms:", len(ms_dirs))

def reduce_table_list(ms_dirs):
    tables = [] 
    for t in ms_dirs:
        if 'table' in os.path.basename(t):
            del(t)
        else:
             #t = os.path.basename(t)
             tables.extend([t])
    return tables

print("Number of Measurement set metadata tables:", len(reduce_table_list(ms_dirs)))

ms_tables = reduce_table_list(ms_dirs)

def check_table_empty(ms_tables):
    good_tables = []
    for t in ms_tables:
        tb.open(t)
        if tb.nrows() != 0:
            #print(tb.colnames())
            print(os.path.basename(tb.name()),':',tb.nrows())
            good_tables.extend([t])
    return(good_tables)

non_zero_tables = check_table_empty(ms_tables)
