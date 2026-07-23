import numpy as np
import fsspec
import pyfive

# =============================================================================
# Configuration
# =============================================================================

ACCESS_METHOD = "https"      # "https" or "s3"
DATASET_NAME = "clw"         # Variable of interest, print again at bottom of script

# -----------------------------------------------------------------------------
# S3 configuration
# -----------------------------------------------------------------------------

S3_BUCKET = "bnl"
S3_FILE = "cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"

S3_URL = f"{S3_BUCKET}/{S3_FILE}"

# -----------------------------------------------------------------------------
# HTTPS configuration
# -----------------------------------------------------------------------------

HTTPS_URL = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/RFMIP/MPI-M/MPI-ESM1-2-LR/piClim-spAer-anthro/r1i1p1f2/Amon/clw/gn/v20190710/clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"
HTTPS_FILE = "clw_Amon_MPI-ESM1-2-LR_piClim-spAer-anthro_r1i1p1f2_gn_184901-187912.nc"

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

            print(f"  chunks : {obj.chunks}")

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
