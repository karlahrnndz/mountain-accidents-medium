import pandas as pd
import logging
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

# Input filepaths
EXP_FILEPATH = os.path.join('data', 'input', 'expeditions.csv')
CAT_FILEPATH = os.path.join('data', 'input', 'tags.csv')

# Output filepaths
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')
LABELS_FILEPATH = os.path.join('data', 'input', 'tags.csv')
TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
NO_EXPED_FILEPATH = os.path.join('data', 'output', 'no_exped.csv')

# Other
NO_PEAKS = 5  # Number of peaks to plot
LABEL_THRESHOLD = 0.8
ORIG_LOG_CONFIG = logging.getLogger().getEffectiveLevel()

# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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
key_df.rename(columns={'expid': 'no_exped'}, inplace=True)
key_df.sort_values(by='no_exped', ascending=False, inplace=True, ignore_index=True)
key_df = key_df.iloc[:NO_PEAKS, :]

# Save number of expeditions for plotting
key_df.to_csv(NO_EXPED_FILEPATH, index=False)

acc_df = key_df[['peakid']].merge(exp_df[['peakid', 'accidents']], how='left', on='peakid')
acc_df.dropna(subset=['accidents'], inplace=True, ignore_index=True)

# Save acc_df (one time only)
acc_df.reset_index(inplace=True)
acc_df.rename(columns={'index': 'acc_id'}, inplace=True)
acc_df.to_csv(ACCIDENT_FILEPATH, index=False)
