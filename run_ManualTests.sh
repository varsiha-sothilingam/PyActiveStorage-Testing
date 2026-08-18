#!/usr/bin/env bash
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

#python tests/test_real_https.py  3>&1 1>>"gws-server-https-test-$(date +%Y%m%d-%H%M%S).output" 2>&1
#python tests/test_real_https.py 2>&1 | tee "debugJSON-https-test-$(date +%Y%m%d-%H%M%S).output"


#python tests/test_debug_https.py  3>&1 1>>"compareJSONResponses-$(date +%Y%m%d-%H%M%S).output" 2>&1
python scripts/test_debug_https.py  3>&1 1>>"esgf-ceda-httpsServerStressTest-$(date +%Y%m%d-%H%M%S).output" 2>&1



#usr/bin/time -l python scripts/run_new_tenancy.py

#http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc
https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc
https://esgf.ceda.ac.uk/thredds/catalog/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/catalog.html?dataset=esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc

https://esgf.ceda.ac.uk/thredds/catalog/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/catalog.html?dataset=esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/cl_Amon_UKESM1-0-LL_esm-hist_r1i1p1f2_gn_185001-189912.nc


https://esgf.ceda.ac.uk/thredds/catalog/esg_cmip6/CMIP6/CMIP/MOHC/UKESM1-0-LL/esm-hist/r1i1p1f2/Amon/cl/gn/v20190723/catalog.html


http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/MOHC/UKESM1-0-LL/1pctCO2/r1i1p1f2/Amon/clw/gn/v20190406/clw_Amon_UKESM1-0-LL_1pctCO2_r1i1p1f2_gn_185001-189912.nc

http://esgf3.dkrz.de/thredds/dodsC/cmip6/C4MIP/MOHC/UKESM1-0-LL/1pctCO2-rad/r1i1p1f2/Amon/hur/gn/v20190723/hur_Amon_UKESM1-0-LL_1pctCO2-rad_r1i1p1f2_gn_185001-194912.nc