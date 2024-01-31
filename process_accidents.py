import pandas as pd
import logging
import os

# Input filepaths
EXP_FILEPATH = os.path.join('data', 'input', 'expeditions.csv')
CAT_FILEPATH = os.path.join('data', 'input', 'labels.csv')

# Output filepaths
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')
LABELS_FILEPATH = os.path.join('data', 'input', 'labels.csv')
TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')

# Other
NO_PEAKS = 5  # Number of peaks to plot
LABEL_THRESHOLD = 0.8
ORIG_LOG_CONFIG = logging.getLogger().getEffectiveLevel()


# ----------------------------------------------------------------------------------- #
#                                 Initial Data Processing                             #
# ----------------------------------------------------------------------------------- #

# Load expeditions data
exp_df = pd.read_csv(EXP_FILEPATH)
exp_df.dropna(subset=['peakid'], inplace=True, ignore_index=True)

# Create unique expid column
exp_df['expid'] = exp_df['expid'] + '-' + exp_df['year'].astype('str')

# Find peaks with the highest number of expeditions and extract the data
key_df = exp_df.groupby(by=['peakid'])['expid'].count().reset_index()
key_df.sort_values(by='expid', ascending=False, inplace=True, ignore_index=True)
key_df = key_df.iloc[:NO_PEAKS, :]
acc_df = key_df[['peakid']].merge(exp_df[['peakid', 'accidents']], how='left', on='peakid')
acc_df.dropna(subset=['accidents'], inplace=True, ignore_index=True)

# Save acc_df (one time only)
acc_df.reset_index(inplace=True)
acc_df.rename(columns={'index': 'acc_id'}, inplace=True)
acc_df.to_csv(ACCIDENT_FILEPATH, index=False)