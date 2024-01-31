
import pandas as pd
import os

# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
TAGGED_ACC_EXP_FILEPATH = os.path.join('data', 'output', 'tagged_accidents_exp.csv')
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')


# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------- #
#                                    Analyze Tags                                     #
# ----------------------------------------------------------------------------------- #


# Load accident descriptions
tagged_df = pd.read_csv(TAGGED_ACC_FILEPATH)

# Explode tags
tagged_df['tags'] = tagged_df['tags'].apply(eval)
tagged_df = tagged_df.explode('tags', ignore_index=True)

# Add accident information by acc_id
acc_df = pd.read_csv(ACCIDENT_FILEPATH)
tagged_df = tagged_df.merge(acc_df, how='left', on='acc_id')

# Splitting the 'tags' column into two separate columns
tagged_df[['tag', 'prob']] = tagged_df['tags'].apply(pd.Series)
tagged_df.drop(columns=['tags'], inplace=True)

# Save exploded dataframe
tagged_df.to_csv(TAGGED_ACC_EXP_FILEPATH, index=False)

# Count number of occurrences per tag and probability  # TODO – below just for fun
df = tagged_df.loc[tagged_df.prob.ge(0.8), :].copy()
print(df.loc[df.tag.eq('extreme cold') & df.tag.ne('frostbite') & df.tag.ne('hypothermia'), :].head())

print('hi')
