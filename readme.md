# Horizontal velocity decomposer

## Code to find the time-serie of horizontal velocity profile associated with different vertical internal seiche modes 

The mode decomposition is already implemented in version 1.00.4 of Interwave Analyzer. 
However, since the software does not use the velocity data, this data must be combined with outputs from Interwave Analyzer in order to generate the velocity profile associated with each vertical mode. 

To obtain the velocity profile associated with each vertical mode, you must have:

1) Time-series of horizontal velocity profiles;
2) Outputs from Interwave Analyzer, which are:

- mab_decomp.txt;
- time_decomp.txt;
- mab_decomp_oiginal.txt;
- uarbit_decomp_mode#.txt  [# all modes available];
- cpzinho_mode#.txt        [# all modes available];

This code assumes some condition based on velocity data

1) The Original velocity profiles should match the vertical grid of temperature data (applied in the Interwave Analyzer software);
2) The velocity profiles do not need to match the temporal resolution of output results from Interwave Analyzer, but the variable dt_model should have the same value in minutes of the temporal resolution specified in the Interwave Analyzer GUI for decomposition model;
3) Columns and rows represent z and t, respectively. 
