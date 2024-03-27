# Automatic detection of motion artefacts in the ECG signal from a wearable sensor using methods of artificial intelligence
## Master's thesis

### /data
All of the raw ECG data files are located in this directory, the subdirectory /labels contains the files with manually labeled data.
* The filename convention for the raw ECG data located in /data directory is XX_ACTIVITY-TYPE_ELECTRODE-TYPE.csv
* The filename convention for labeled ECG data located in /labels directory is XX_ACTIVITY-TYPE_ELECTRODE-TYPE_SEG-LEN_labels.csv

__ELECTRODE-TYPE encoding:__
* 01    - Ag/AgCl electrodes
* 02    - Chrome-nickel electrodes
* 03    - Textile electrodes

__ACTIVITY-TYPE encoding:__
* 00    - Rest
* 01    - Arm movements
* 02    - Walk 4 km/h
* 03    - Run 8 km/h
* 04    - Squats
* 05    - Unknown

### /src/data_labeler

The script and graphical user interface for manual data labelling are located in this directory. The GUI can be run from the /src directory using the command __python3 data_labeler/data_labeler.py__.

data_labeler.py [-l segment_length] [-f sampling_rate] [-s starting_segment] input_file
* input_file (str)       - input file name, must be a .csv file located in the /data directory
* segment_length (int)   - length of a single segment in seconds, defaults to 5 seconds
* sampling_rate (int)    - sampling frequency of input file, defaults to 500 frames per second
* starting_segment (int) - segment number to display, defaults to fist segment

NOTE: Instead of using the GUI buttons for switching between samples and labelling one can opt to use keyboard shortcuts - left key and right key for switching and space key for toggling the artefact toggle button.


