# PyActiveStorage Testing Suite

This repository contains all items to evaulate performance and stress testing of the PyActiveStorage tool. Various tests are completed and documented for more information about the settings and results.

Due to the nature of the tests there are many scripts and therefore below is an attempt to summarise all scripts and their functionality to not lose track.

## Running scripts

```runTesting.sh```
This is the main running script where one can specifiy the slicing and output directories. It will run the job multiple times in order to account for statistical fluctuations. It automatically runs the second script which converts the log file into a python file with Numpy arrays for the various metrics such as time, CPU usuage and memory usuage. The conda enviroment must be set up manually before running the script

```run_ConcurrencyTests.sh ```
This script runs multiple tests concurrently. It does concurrent tests where each one has a slightly different python version in the conda enviroment. Therefore no conda environment should be setup in advance of running this script. In this test, the * <code><span style="color:gold">test_debug_https.py</span> </code> is ran to perform a stress test.


```run_ManualTests.sh```
To run quick tests by hand and check the output, look through this script for various commands and information.

## Files
```filesList.txt``` 
This is a short summary of files which one can run tests and find locations for both HTTPS Servers and S3 Object Store.


## Directories

1. ```data/```: locally downloaded files for testing. 
2. ```documentation/```: LaTeX for PyActiveStorage documentation, used to record data plots, results and testing conditions in detail. 
3. ```GHA-emulator/```: This is an emulator of the GitHub Action nightly test ran on the PyActiveStorage repo. The emulator allows one to test multiple python versions concurrently and observe test failure rates.
4. ```output/```: All log and python files produced during the running of tests are stored here. 
5. ```outputPlots```: Directory of all plotting scripts for various tests
4. ```scripts/```:  main testing scripts are here to test the pyactivestorage for various testing conditions and settings. 
    * <code><span style="color:gold">getFileInfo.py </span> </code> and <code><span style="color:gold">getFileChunkInfo.py  </span> </code> : The two scripts both function as a reader of files in order to understand file meta in one place for all variables. It uses pyFive to read the b-tree of the file and list out all the variables. Sizes of the file and chunks are also determined. It is slow reading remote so if fast reading is required, download file locally and run through the script. The scripts are compatible with both s3 and https remote files.
    * <code><span style="color:gold">run_new_tenancy.py</span> </code>: This is the main testing script used to measure the performance of the PyActiveStorage. To run, use the running shell scripts. 
    * <code><span style="color:gold">getResults.py</span> </code>: The output log files produced will be converted into python files containing numpy arrays with the parameters of interest for the testing of the PyActiveStorage. 
    * <code><span style="color:gold">test_debug_https.py</span> </code>: This script is ran where the function test_https_stresstest() will increase the slice range until it sees a point failure. This allows for a stress test to be performed. The values are set inside the python script and should be checked by hand if they are appropriate for the file and variable used.
    * <code><span style="color:gold">test_httpsCEDA.py</span> </code>: Script of the MVP to undergo HTTPS server testing with no PyActiveStorage dependencies.   
    * <code><span style="color:gold">getKPI.py</span> </code>: Obselete script which prints out averages of the run time metrics. 
5. ```testingplots```: This is an obsolete data visualisation directory where initial plotting scripts where created to study logs.
