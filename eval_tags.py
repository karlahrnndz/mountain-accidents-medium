from concurrent.futures import ProcessPoolExecutor, as_completed
from transformers import pipeline
import pandas as pd
import logging
import os


# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')

# Load accident descriptions
tagged_df = pd.read_csv(TAGGED_ACC_FILEPATH)

tagged_df['tags'] = tagged_df['tags'].apply(eval)
tagged_df = tagged_df.explode('tags', ignore_index=True)

# acc_df = pd.read_csv(ACCIDENT_FILEPATH)
# tagged_df = tagged_df.merge(acc_df, how='left', on='acc_id')

print('hi')
