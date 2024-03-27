"""Class handling data access for manual ECG labeling"""

__author__      = "Veronika Kalouskova"
__copyright__   = "Copyright 2024, FIT CVUT"

import os
import sys
import math
import pandas as pd
import numpy as np


class DataHandler():

    def __init__(self, filename, fs, seg_len):
        self.FILE_IN = filename
        self.FILE_OUT = '../data/labels/' + filename.split('.')[0] + '_labels_' + str(seg_len) + '.csv'

        self.df_in = self.read_file(filename)
        self.load_data(fs, seg_len)

    #   Load output .csv file if it exists, if not create a new dataframe
    def load_data(self, fs, seg_len):
        if os.path.exists(self.FILE_OUT):
            self.df_out = pd.read_csv(self.FILE_OUT, sep=';')
        else:
            self.create_df(fs, seg_len)

    #   Create output dataframe
    def create_df(self, fs, seg_len):
            data_size = len(self.df_in['value'])

            seg_len_pts = seg_len * fs
            rows = math.floor(data_size / seg_len_pts)

            start = np.arange(0, data_size - seg_len_pts, seg_len_pts)
            end = np.arange(seg_len_pts, data_size, seg_len_pts)
            type, _ = self.get_activity_type()

            # Initialize pandas dataframe for output data
            self.df_out = pd.DataFrame(index=range(rows), columns=['start', 'end', 'activity', 'artifact'])

            self.df_out['start'] = start
            self.df_out['end'] = end
            self.df_out['activity'] = type

            # Default values based on activity type - rest defaults to no artifact, other activities to artifact present
            if (type == 0):
                self.df_out['artifact'] = 0
            else:
                self.df_out['artifact'] = 1

    #   Set value of artifact based on radio button selection
    def set_artifact(self, seg_curr, label):
        self.df_out.at[seg_curr, 'artifact']  = int(label)
        self.df_out.to_csv(self.FILE_OUT, sep=';', index=False)  

        print(self.df_out)

    #   Get value of artifact at current selection  
    def get_artifact(self, seg_curr):
        if pd.isna(self.df_out.at[seg_curr, 'artifact']):
            self.set_artifact(seg_curr, 0)
        
        return self.df_out.at[seg_curr, 'artifact']
   
    #   Determine activity type based on filename
    def get_activity_type(self):
        if 'klud' in self.FILE_IN:
            return 0, 'REST'
        elif 'ruky' in self.FILE_IN:
            return 1, 'ARM MOVEMENTS'
        elif 'chodza' in self.FILE_IN:
            return 2, 'WALK 4 km/h'
        elif 'beh' in self.FILE_IN:
            return 3, 'RUN 8 km/h'
        elif 'drepy' in self.FILE_IN:
            return 4, 'SQUATS'
        else:
            return 5, 'UNKNOWN'

    #   Read input .csv file, handle possible exceptions
    def read_file(self, filename):
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
