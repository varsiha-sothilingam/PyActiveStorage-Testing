import os
import numpy as np
import fsspec
import pyfive

# S3 credentials & file
S3_BUCKET = "bnl"
bigger_file  = "cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"  
dataset_name = "clw" 
#Available datasets: ['time', 'bnds', 'time_bnds', 'lev', 'lev_bnds', 'b', 'orog', 'b_bnds', 'lat', 'lat_bnds', 'lon', 'lon_bnds', 'cl']
s3_url = f"{S3_BUCKET}/{bigger_file}"

# Create S3 filesystem
fs = fsspec.filesystem(
    "s3",
    key="f2d55c6dcfc7618b2c34e00b58df3cef",
    secret="$/'#M{0{/4rVhp%n^(XeX$q@y#&(NM3W1->~N.Q6VP.5[@bLpi='nt]AfH)>78pT",
    client_kwargs={"endpoint_url": "https://uor-aces-o.s3-ext.jc.rl.ac.uk"}
)

#
https_url = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/HighResMIP/MPI-M/MPI-ESM1-2-HR/control-1950/r1i1p1f1/Amon/hur/gn/v20180524/hur_Amon_MPI-ESM1-2-HR_control-1950_r1i1p1f1_gn_195001-195012.nc"
https_url = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/ssp370SST-lowNTCF/r1i1p1f2/Amon/cl/gn/v20200420/cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_201501-204912.nc" 
https_url = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-1-LL/piControl/r1i1p1f2/Amon/ta/gn/latest/ta_Amon_UKESM1-1-LL_piControl_r1i1p1f2_gn_274301-274912.nc"


https_url = "https://gws-access.jasmin.ac.uk/public/ukesm/TerraFIRMA/esm-piControl/r1i1p1f1/Amon/ta/gn/v20241002/ta_Amon_UKESM1-2-LL_esm-piControl_r1i1p1f1_gn_210001-214912.nc"
https_url = "https://gws-access.jasmin.ac.uk/public/canari/varsiha/clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
#https_url = "https://gws-access.jasmin.ac.uk/public/canari/varsiha/tas_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
https_url = "https://gws-access.jasmin.ac.uk/public/canari/varsiha/cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"


https_url = "https://esgf3.dkrz.de/thredds/dodsC/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/cl/gn/v20190710/cl_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
https_url = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/hur/gn/v20190710/hur_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
https_url = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/LS3MIP/MPI-M/MPI-ESM1-2-LR/amip-lfmip-pdLC/r1i1p1f2/Amon/wap/gn/v20190815/wap_Amon_MPI-ESM1-2-LR_amip-lfmip-pdLC_r1i1p1f2_gn_198001-199912.nc"

https_url = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/tas/gn/v20190710/tas_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
https_url = "https://esgf.ceda.ac.uk/thredds/catalog/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/catalog.html?dataset=esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"

https_url = "https://esgf3.dkrz.de/thredds/dodsC/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/cl/gn/v20190710/cl_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
https_url = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/clw/gn/v20190710/clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
#https_url = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_185001-189912.nc"


https_url = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_185001-189912.nc"
https_url = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/clw/gn/v20190710/clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"



fs = fsspec.filesystem("http")

file_info = fs.info(https_url)

#  Get and print file size
#file_info = fs.info(s3_url)
file_size_bytes = file_info["size"]
print(f"File: {bigger_file}")
print(f"File size: {file_size_bytes} bytes ({(file_size_bytes /(1024**2)/1000):.2f}  GB)")

with fs.open(https_url, "rb") as f:
    with pyfive.File(f) as h5:
        # Access the dataset directly by name
        if dataset_name in h5:
            ds = h5[dataset_name]
            print(f"Dataset: {dataset_name}")
            print(f"Shape: {ds.shape}")
            print(f"Chunk shape: {ds.chunks}")
            
            # Compute number of chunks per axis
            if ds.chunks is not None:
                num_chunks_per_axis = [int(np.ceil(ds.shape[i] / ds.chunks[i])) for i in range(len(ds.shape))]
                total_chunks = np.prod(num_chunks_per_axis)
                print(f"Chunks per axis: {num_chunks_per_axis}")
                print(f"Total number of chunks: {total_chunks}")
                
                # Estimate chunk size in bytes
                chunk_size_bytes = np.prod(ds.chunks) * ds.dtype.itemsize
                print(f"Approx chunk size in bytes: {chunk_size_bytes} ({(chunk_size_bytes /(1024**2)):.2f}  MB) ")
            else:
                print("Dataset is not chunked.")
        else:
            print(f"Dataset '{dataset_name}' not found in the file.")
            print(f"Available datasets: {list(h5.keys())}")


        