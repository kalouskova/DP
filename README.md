# Automatic detection of motion artefacts in the ECG signal from a wearable sensor using methods of artificial intelligence
## Master's thesis

### /data
All of the raw ECG data files are located in this directory. There is a separate numbered directory for each of the subjects, the subdirectory /labels contains files with manually labeled data.
* The filename convention for the ECG data located in */data/XX* directory is  
*XX_ELECTRODE-TYPE_ACTIVITY-TYPE.csv*
* The filename convention for corresponding ECG data labels located in */data/XX/labels* directory is  
*XX_ELECTRODE-TYPE_ACTIVITY-TYPE_SEG-LEN.csv*

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

The script and graphical user interface for manual data labelling are located in this directory. The GUI can be run from the */data_labeler* directory using the command __python3 data_labeler.py__.

data_labeler.py [-l segment_length] [-f sampling_rate] [-s starting_segment] input_file
* input_file (str)       - input file name, must be a .csv file located in the /data directory
* segment_length (int)   - length of a single segment in seconds, defaults to 5 seconds
* sampling_rate (int)    - sampling frequency of input file, defaults to 500 frames per second
* starting_segment (int) - segment number to display, defaults to fist segment

Labels automatically default to artefact present for all activities besides rest, which defaults to no artefact. There is no need to save the labels, the output .csv file is updated after each artefact button toggle.

__NOTE: *Instead of using the GUI buttons for switching between samples and labelling one can opt to use keyboard shortcuts - left key and right key for switching, space key for toggling the artefact toggle button, enter key for leaving the application.*__


