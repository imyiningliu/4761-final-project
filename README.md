# 4761-final-project

## Description
`D-statistic.py`: compute D-statistic benchmark from symbols 

`generate-simulation-data.py`: reproduce simulated data (symbols and genealogies); random seed was 3; sample data files are in `./data` 

`simulation.py`: simulate genealogies using msprime 

`utils.py`: miscellaneous functions for computing emission/transition probabilities, converting between times, converting tree sequence to symbols 

`model.py`: HMM model to model introgression regions 

## System Requirements
Python 3.8.3 was used for this project. 

Add-on libraries: `hmmlearn`, `msprime`. 

No additional computing resources was used for directly working with symbols; the results on `length = 10^6` was ran on google cloud VM. 
