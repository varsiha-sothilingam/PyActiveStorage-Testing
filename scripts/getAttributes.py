
from netCDF4 import Dataset

#trying to locate files in catalogue 
file_path = "cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"

with Dataset(file_path, "r") as ds:
    print("Global attributes:\n")
    
    for attr in ds.ncattrs():
        value = getattr(ds, attr)
        print(f"{attr}: {value}")

import cf
x = cf.read('cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc')
print( x.properties())