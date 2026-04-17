#!/bin/bash
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
# --- CONFIGURATION ---
TARGET_FILE="ch330a.pc19790301-def.nc"
TARGET_VAR="UM_m01s16i202_vn1106"

# Define slices as a simple comma-separated string: start,stop,start,stop...
#Target 1     
#SLICES_STR="0,8,0,413,0,551"
#Target 5
#SLICES_STR="0,14,0,707,0,942"        
#Target 10    
#SLICES_STR="0,18,0,891,0,1188"  
#Target 25    
#SLICES_STR="0,25,0,1209,0,1612"
#Target 50    
#SLICES_STR="0,31,0,1525,0,2032" 
#Target 75    
#SLICES_STR="0,36,0,1753,0,2337"
#Target 100
SLICES_STR="0,40,0,1920,0,2560"

#SLICES_STR="0,300,0,85,0,144,0,192"

TEST_NO="test_s3_Target50-Without-AXIS_Active"
# Automatically create a unique name for this run
BASE_NAME="f_${TARGET_FILE}_var_${TARGET_VAR}_slice_${SLICES_STR//,/_}"
LOGFILE="output/CountMemTest/${TEST_NO}_${BASE_NAME}.log.output"
PY_OUT="output/CountMemTest/${TEST_NO}_${BASE_NAME}.py"

> "$LOGFILE"

# --- EXECUTION ---
for i in {1..2}
do
  echo "Run $i:" >> "$LOGFILE"
  # Pass the variables to Python here
  /usr/bin/time -l python scripts/run_new_tenancy.py \
    "$TARGET_FILE" \
    "$TARGET_VAR" \
    "$SLICES_STR" >> "$LOGFILE" 2>&1
  
  echo "----------------------" >> "$LOGFILE"
done

# --- POST-PROCESSING ---
python scripts/getResults.py -i "$LOGFILE" -o "$PY_OUT"

echo "Process Complete."
echo "Log: $LOGFILE"
echo "Result: $PY_OUT"