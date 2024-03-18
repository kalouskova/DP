"""Data handler for manual ECG labeling"""

__author__      = "Veronika Kalouskova"
__copyright__   = "Copyright 2024, FIT CVUT"

import os
import sys
import math
import pandas as pd
import numpy as np


class DataHandler():

    def __init__(self, filename, data_size, fs, seg_len):
        self.FILE_IN = filename
        self.FILE_OUT = '../data/labels/' + filename.split('.')[0] + '_' + str(fs) + '_' + str(seg_len) + '_labels.csv'

        self.load_data(data_size, fs, seg_len)

    #   Load output .csv file if it exists, if not create a new dataframe
    def load_data(self, data_size, fs, seg_len):
        if os.path.exists(self.FILE_OUT):
            self.df = pd.read_csv(self.FILE_OUT, sep=';')
        else:
            seg_len_pts = seg_len * fs
            rows = math.floor(data_size / seg_len_pts)

            start = np.arange(0, data_size - seg_len_pts, seg_len_pts)
            end = np.arange(seg_len_pts, data_size, seg_len_pts)
            type, _ = self.get_activity_type()

            # Initialize pandas dataframe for output data
            self.df = pd.DataFrame(index=range(rows), columns=['start', 'end', 'activity', 'artifact'])

            self.df['start'] = start
            self.df['end'] = end
            self.df['activity'] = type

    #   Set value of artifact based on radio button selection
    def set_artifact(self, seg_curr, label):
        self.df.at[seg_curr, 'artifact']  = label
        self.df.to_csv(self.FILE_OUT, sep=';', index=False)  

        print(self.df)

    #   Get value of artifact at current selection  
    def get_artifact(self, seg_curr):
        if pd.isna(self.df.at[seg_curr, 'artifact']):
            self.set_artifact(seg_curr, 0)
        
        return self.df.at[seg_curr, 'artifact']
   
    #   Determine activity type based on filename
    def get_activity_type(self):
        if 'rest' in self.FILE_IN:
            return 0, 'REST'
        elif 'walk' in self.FILE_IN:
            return 1, 'WALK'
        elif 'run5' in self.FILE_IN:
            return 2, 'RUN 5 km/h'
        elif 'squats' in self.FILE_IN:
            return 3, 'SQUATS'
        else:
            return 4, 'UNKNOWN'


#   Read input .csv file, handle possible exceptions
def read_file(filename):
    try:
        input_data = pd.read_csv('../data/' + filename, sep=';', names=['timestamp', 'value'])
    except FileNotFoundError:
        print('File not found.')
        sys.exit(1)
    except pd.errors.ParserError:
        print('Parse error.')
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print('Empty file.')
        sys.exit(1)
    
    return input_data
