import matplotlib.pyplot as plt
import pandas as pd
import json
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
TAGGED_ACC_FIN_FILEPATH = os.path.join('data', 'output', 'tagged_accidents_final.csv')
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')
TAGS_FILEPATH = os.path.join('data', 'input', 'tags.csv')
TAG_MAP_FILEPATH = os.path.join('data', 'input', 'tag_map.json')
TAG_COUNT_FILEPATH = os.path.join('data', 'output', 'tag_count.csv')

# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------- #
#                         Prepare Tagged Accident Information                         #
# ----------------------------------------------------------------------------------- #

# Load accident tags
tagged_df = pd.read_csv(TAGGED_ACC_FILEPATH)

# Explode tags
tagged_df['tags'] = tagged_df['tags'].apply(eval)
tagged_df = tagged_df.explode('tags', ignore_index=True)

# Splitting the 'tags' column into two separate columns
tagged_df[['tag', 'prob']] = tagged_df['tags'].apply(pd.Series)
tagged_df.drop(columns=['tags'], inplace=True)

# Drop NAs
tagged_df.dropna(subset='tag', inplace=True, ignore_index=True)

# Add tag_id column
tag_df = pd.read_csv(TAGS_FILEPATH)
tagged_df = tagged_df.merge(tag_df, how='left', on='tag')

# Add accident information by acc_id
acc_df = pd.read_csv(ACCIDENT_FILEPATH)
tagged_df = tagged_df.merge(acc_df, how='left', on='acc_id')
tagged_df['tag_id'] = tagged_df['tag_id'].astype(int)


# ----------------------------------------------------------------------------------- #
#                              Custom Map & Remove Tags                               #
# ----------------------------------------------------------------------------------- #

# Remove "extreme cold" tag, and cases where accident description was "Nothing"
tagged_df = tagged_df.query('tag != "extreme cold"')
tagged_df = tagged_df.query('accidents != "Nothing"')
tagged_df.reset_index(inplace=True, drop=True)

# Look at value count distributions for high-probability tags
plt.figure(figsize=(10, 6))
tagged_df['tag'].value_counts().plot(kind='bar', color='#ca0203')
plt.tight_layout()
plt.savefig(os.path.join('data', 'output', 'tag_value_counts.svg'), format='svg')
plt.show()

# Apply custom maps
with open(TAG_MAP_FILEPATH, 'r') as json_file:
    tag_map = json.load(json_file)

tagged_df['new_tag'] = tagged_df['tag'].apply(lambda x: tag_map[x] if x in tag_map else x)

filtered_df = tagged_df[['new_tag', 'acc_id']]
filtered_df.drop_duplicates(inplace=True)

# Look at value count distributions
plt.figure(figsize=(10, 6))
filtered_df['new_tag'].value_counts().plot(kind='bar', color='#f2b202')
plt.tight_layout()
plt.savefig(os.path.join('data', 'output', 'updated_tag_value_counts.svg'), format='svg')
plt.show()

filtered_df = filtered_df.query('new_tag != "inadequate preparation"')
filtered_df = filtered_df.query('new_tag != "steep rock"')
tagged_df = tagged_df.query('new_tag != "inadequate preparation"')
tagged_df = tagged_df.query('new_tag != "steep rock"')

# Look at value count distributions
plt.figure(figsize=(10, 6))
filtered_df['new_tag'].value_counts().plot(kind='bar', color='#01a0e6')
plt.tight_layout()
plt.savefig(os.path.join('data', 'output', 'final_tag_value_counts.svg'), format='svg')
plt.show()


# Save exploded dataframe for top 10 tags
top10_df = filtered_df['new_tag'].value_counts().iloc[:10].reset_index()
top10_df.drop(columns=['count'], inplace=True)
save_df = top10_df.merge(tagged_df, how='left', on='new_tag')
save_df.drop(columns=['tag', 'prob', 'tag_id'], inplace=True)
save_df.drop_duplicates(inplace=True)
save_df.to_csv(TAGGED_ACC_FIN_FILEPATH, index=False)
