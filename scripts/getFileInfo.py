import os
import numpy as np
import fsspec
import pyfive

# S3 credentials & file
S3_BUCKET = "bnl"
bigger_file  = "ta_Amon_UKESM1-1-LL_piControl_r1i1p1f2_gn_274301-274912.nc "  
dataset_name = "ta" 

s3_url = f"{S3_BUCKET}/{bigger_file}"

# Create S3 filesystem
fs = fsspec.filesystem(
    "s3",
    key="f2d55c6dcfc7618b2c34e00b58df3cef",
    secret="$/'#M{0{/4rVhp%n^(XeX$q@y#&(NM3W1->~N.Q6VP.5[@bLpi='nt]AfH)>78pT",
    client_kwargs={"endpoint_url": "https://uor-aces-o.s3-ext.jc.rl.ac.uk"}
)

#  Get and print file size
file_info = fs.info(s3_url)
file_size_bytes = file_info["size"]
print(f"File: {bigger_file}")
print(f"File size: {file_size_bytes} bytes ({(file_size_bytes /(1024**2)/1000):.2f}  GB)")

with fs.open(s3_url, "rb") as f:
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
                print(f"Approx chunk size in bytes: {chunk_size_bytes}")
            else:
                print("Dataset is not chunked.")
        else:
            print(f"Dataset '{dataset_name}' not found in the file.")