#!/bin/bash
#python compareHistos.py \
#-i1 ../output/f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_MT_100_Net_UoREth_Slice_0_30_0_30_0_30.py \
#-i2 ../output/f_ch330a.pc19790301-bnl.nc_var_UM_m01s30i202_vn1106_MT_100_Net_UoREth_Slice_0_30_0_30_0_30.py \
#-o histogram_m01s16i202_m01s30i202.pdf



python  testingReportPlots.py \
-i1 ../output/f_ch330a.pc19790301_bnl.nc_var_UM_m01s16i202_vn1106_MT_100_Net_UoREth_Slice_0_30_0_30_0_30.py \
-i2 ../output/f_ch330a.pc19790301-bnl.nc_var_UM_m01s16i202_vn1106_MT_100_Net_UoRWiFi_Slice_0_30_0_30_0_30.py \
-o testScript.pdf
