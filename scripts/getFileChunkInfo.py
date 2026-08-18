import numpy as np
import fsspec
import pyfive

# =============================================================================
# Configuration
# =============================================================================

ACCESS_METHOD = "https"      # "https" or "s3"
DATASET_NAME = "cl"         # Variable of interest, print again at bottom of script

# -----------------------------------------------------------------------------
# S3 configuration
# -----------------------------------------------------------------------------

S3_BUCKET = "bnl"
S3_FILE = "cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"

S3_URL = f"{S3_BUCKET}/{S3_FILE}"

# -----------------------------------------------------------------------------
# HTTPS configuration
# -----------------------------------------------------------------------------

#HTTPS_URL  = "https://gws-access.jasmin.ac.uk/public/canari/varsiha/cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"
#HTTPS_URL  = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/ssp370SST-lowNTCF/r1i1p1f2/Amon/cl/gn/latest/cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"
#HTTPS_FILE = "cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"

#HTTPS_URL  = "http://esgf-node.ornl.gov/thredds/fileServer/css03_data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/Amon/tas/gn/v20190429/tas_Amon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc"
#HTTPS_FILE = "tas_Amon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc"

#HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"
#HTTPS_FILE = "cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"


HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_195001-199912.nc"
HTTPS_FILE = "clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_195001-199912.nc"

HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/clw/gn/v20211103/clw_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_185001-189912.nc"
HTTPS_FILE = "clw_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_185001-189912.nc"


HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/hur/gn/v20211103/hur_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_215001-224912.nc"
HTTPS_FILE = "hur_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_215001-224912.nc"


HTTPS_URL = "http://esgf3.dkrz.de/thredds/dodsC/cmip6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp245/r14i1p1f1/CFmon/hur/gn/v20210901/hur_CFmon_MPI-ESM1-2-LR_ssp245_r14i1p1f1_gn_201501-203412.nc"
HTTPS_FILE = "hur_CFmon_MPI-ESM1-2-LR_ssp245_r14i1p1f1_gn_201501-203412.nc"

#test
#HTTPS_URL = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"

HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_195001-199912.nc"
HTTPS_FILE = "clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_195001-199912.nc"

#HTTPS_URL =  "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_185001-189912.nc"
#HTTPS_FILE = "clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_185001-189912.nc"

HTTPS_URL =   "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/clw/gn/v20190710/clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
HTTPS_FILE = "clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"


"""
cl
  shape  : (600, 85, 144, 192)
  dtype  : float32
  chunk size : (1, 43, 72, 96)
  chunk grid   : [600, 2, 2, 2]
  total chunks : 4800
  chunk size   : 1,188,864 bytes (1.13 MB)
"""

#HTTPS_URL = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"

"""
cl
  shape  : (600, 85, 144, 192)
  dtype  : float32
  chunk size : (1, 43, 72, 96)
  chunk grid   : [600, 2, 2, 2]
  total chunks : 4800
  chunk size   : 1,188,864 bytes (1.13 MB)
"""

#HTTPS_URL = "https://gws-access.jasmin.ac.uk/public/canari/varsiha/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"

#HTTPS_FILE = "cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc"



# =============================================================================
# Create filesystem
# =============================================================================

if ACCESS_METHOD.lower() == "s3":

    fs = fsspec.filesystem(
        "s3",
        key="YOUR_KEY",
        secret="YOUR_SECRET",
        client_kwargs={
            "endpoint_url": "https://uor-aces-o.s3-ext.jc.rl.ac.uk"
        },
    )

    filename = S3_FILE
    filepath = S3_URL

elif ACCESS_METHOD.lower() == "https":

    fs = fsspec.filesystem("http")
    filename = HTTPS_FILE
    filepath = HTTPS_URL

else:
    raise ValueError("ACCESS_METHOD must be 'https' or 's3'")

# =============================================================================
# File information
# =============================================================================

file_info = fs.info(filepath)

file_size = file_info["size"]

print("=" * 80)
print(f"File: {filename}")
print(f"Access: {ACCESS_METHOD}")
print(f"Size : {file_size:,} bytes ({file_size / 1024**3:.2f} GB)")
print("=" * 80)

# =============================================================================
# Open file
# =============================================================================

with fs.open(filepath, "rb") as f:

    with pyfive.File(f) as h5:

        print("\nVariables in file:")
        print("-" * 80)
        for name in h5.keys():
            print(name)

        for name in h5.keys():

            obj = h5[name]

            # Skip groups
            if not hasattr(obj, "shape"):
                print(f"{name:<20} (group)")
                continue

            print(f"\n{name}")
            print(f"  shape  : {obj.shape}")
            print(f"  dtype  : {obj.dtype}")

            if obj.chunks is None:
                print("  chunks : contiguous")
                continue

            print(f"  chunk size : {obj.chunks}")

            chunks_per_axis = [
                int(np.ceil(s / c))
                for s, c in zip(obj.shape, obj.chunks)
            ]

            total_chunks = int(np.prod(chunks_per_axis))

            chunk_bytes = (
                np.prod(obj.chunks)
                * obj.dtype.itemsize
            )

            print(f"  chunk grid   : {chunks_per_axis}")
            print(f"  total chunks : {total_chunks}")
            print(
                f"  chunk size   : "
                f"{chunk_bytes:,} bytes "
                f"({chunk_bytes / 1024**2:.2f} MB)"
            )

# =============================================================================
# Optional: print one dataset in more detail
# =============================================================================

print("\n" + "=" * 80)

with fs.open(filepath, "rb") as f:

    with pyfive.File(f) as h5:

        if DATASET_NAME in h5:

            ds = h5[DATASET_NAME]

            print(f"Selected dataset: {DATASET_NAME}")
            print(f"Shape : {ds.shape}")
            print(f"Dtype : {ds.dtype}")
            print(f"Chunks: {ds.chunks}")

        else:
            print(f"Dataset '{DATASET_NAME}' not found.")
