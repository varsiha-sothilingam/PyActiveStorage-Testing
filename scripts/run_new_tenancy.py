import os
import numpy as np
import sys
from activestorage.active import Active

S3_BUCKET = "bnl"

def test_s3_file(filename, variable, sample_slice):
    """
    Run the test with parameterized file, variable, and slicing via s3
    """
    storage_options = {
        'key': "f2d55c6dcfc7618b2c34e00b58df3cef",
        'secret': "$/'#M{0{/4rVhp%n^(XeX$q@y#&(NM3W1->~N.Q6VP.5[@bLpi='nt]AfH)>78pT",
        'client_kwargs': {'endpoint_url': "https://uor-aces-o.s3-ext.jc.rl.ac.uk"},  # final proxy
    }

    # Reductionist on Wacasoft (behind firewall)
    active_storage_url = "https://reductionist.jasmin.ac.uk/" 
    #active_storage_url = "https://wacasoft1.jasmin.ac.uk/"

    # Construct the URI using the passed filename
    test_file_uri = os.path.join(S3_BUCKET,filename)
    
    print(f"S3 Test file path: {test_file_uri}")
    print(f"Target Variable: {variable}")

    active = Active(
        test_file_uri, 
        variable, 
        interface_type="s3",
        storage_options=storage_options,
        active_storage_url=active_storage_url,
        option_disable_chunk_cache=False
    )

    active._version = 2
    active._method = "min"

    result = active[sample_slice]
    #result = active.mean(axis=(1,2))[sample_slice]
    print("Confirm slice is", sample_slice)   
    print("Result is", result)
    return result


def test_https_file():
    """
    Run the test with parameterized file, variable, and slicing via https
    """
    active_storage_url = "https://reductionist.jasmin.ac.uk/"
    test_file_uri = "https://esgf.ceda.ac.uk/thredds/fileServer/esg_cmip6/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/ssp370SST-lowNTCF/r1i1p1f2/Amon/cl/gn/v20200420/cl_Amon_UKESM1-0-LL_ssp370SST-lowNTCF_r1i1p1f2_gn_205001-209912.nc"
    active = Active(test_file_uri, ncvar="cl",  active_storage_url=active_storage_url, option_disable_chunk_cache=True)
    active._version = 2
    active._method = "min"
    active._max_threads = 100
  
    #result = active[0:40, 0:1920, 0:30, 0:30][0]
    #dataset cl: 600, 85, 144, 192
    result = active[0:40,:,:,:]#0:600,0:85,0:144,0:192]
    print(result)

    return result


if __name__ == "__main__":

    #----------------------------------------------------
    #   s3 access
    #----------------------------------------------------

    # Check if we got the right number of arguments
    """
    if len(sys.argv) < 4:
        print("Usage: python script.py <file> <var> <slices_string>")
        sys.exit(1)

    target_file = sys.argv[1]
    target_var  = sys.argv[2]
    
    # Convert the string "(0,4,0,1,0,30,0,30)" back into slice objects
    # We split the string by commas and group them in pairs
    slice_data = [int(x) for x in sys.argv[3].strip("()").split(",")]
    active_slices = tuple(slice(slice_data[i], slice_data[i+1]) 
                          for i in range(0, len(slice_data), 2))

    final_result = test_s3_file(target_file, target_var, active_slices)
    """
    #----------------------------------------------------
    #  https access- don't bother with the runTesting.sh, just do it manually
    #----------------------------------------------------  

    test_https_file()