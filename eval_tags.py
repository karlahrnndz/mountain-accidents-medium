import matplotlib.pyplot as plt
import pandas as pd
import json
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
TAGGED_ACC_EXP_FILEPATH = os.path.join('data', 'output', 'tagged_accidents_exp.csv')
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')
TAGS_FILEPATH = os.path.join('data', 'input', 'tags.csv')
TAG_MAP_FILEPATH = os.path.join('data', 'input', 'tag_map.json')
TAG_COUNT_FILEPATH = os.path.join('data', 'output', 'tag_count.csv')
NO_TAGS_PLOT = 10
PROB_THRESH = 0.7


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

# Add tag_id column
tag_df = pd.read_csv(TAGS_FILEPATH)
tagged_df = tagged_df.merge(tag_df, how='left', on='tag')

# Drop NAs
tagged_df.dropna(subset='tag', inplace=True, ignore_index=True)

# Add accident information by acc_id
acc_df = pd.read_csv(ACCIDENT_FILEPATH)
tagged_df = tagged_df.merge(acc_df, how='left', on='acc_id')
tagged_df['tag_id'] = tagged_df['tag_id'].astype(int)


# ----------------------------------------------------------------------------------- #
#                             Check For Unnecessary Tags                              #
# ----------------------------------------------------------------------------------- #

# Find unnecessary tags
data_matrix = pd.crosstab(tagged_df['acc_id'], tagged_df['tag_id'])
tags = list(tagged_df['tag_id'].unique())
unnecessary_tags = []

for tag_x in tags:

    # Find tags that are always implied by the presence of tag_x
    implied_by_x = [tag for tag in tags if
                    tag != tag_x and (data_matrix[tag_x] <= data_matrix[tag]).all()]

    # Find tags whose presence always implies the presence of tag_x
    imply_x = [tag for tag in tags if
               tag != tag_x and (data_matrix[tag_x] >= data_matrix[tag]).all()]

    # Check if the sets of inferred_by_tags and imply_x are equal
    if len(implied_by_x) > 0 and (set(implied_by_x) == set(imply_x)):
        unnecessary_tags.append(tag_x)

# Print the list of unnecessary tags
print("Unnecessary Tags:", unnecessary_tags)


# ----------------------------------------------------------------------------------- #
#                                  Custom Map Tags                                    #
# ----------------------------------------------------------------------------------- #

# Look at value count distributions for high-probability tags
filtered_df = tagged_df.query(f'prob >= {PROB_THRESH}')
plt.figure(figsize=(10, 6))
filtered_df['tag'].value_counts().plot(kind='bar', color='skyblue')
plt.xlabel('Tags')
plt.ylabel('Count')
plt.title(f'Histogram of Tag Counts with prob >= {PROB_THRESH}')
plt.tight_layout()
plt.show()

# Apply custom maps
with open(TAG_MAP_FILEPATH, 'r') as json_file:
    tag_map = json.load(json_file)

tagged_df['new_tag'] = tagged_df['tag'].apply(lambda x: tag_map[x] if x in tag_map else x)

# Look at value count distributions for high-probability tags

filtered_df = tagged_df.query(f'prob >= {PROB_THRESH}')
filtered_df.drop(columns=['tag', 'prob', 'tag_id', 'accidents'], inplace=True)
filtered_df.drop_duplicates(inplace=True, ignore_index=True)

plt.figure(figsize=(10, 6))
filtered_df['new_tag'].value_counts().plot(kind='bar', color='skyblue')
plt.xlabel('New Tags')
plt.ylabel('Count')
plt.title(f'Histogram of New Tag Counts with prob >= {PROB_THRESH}')
plt.tight_layout()
plt.show()

# Save exploded dataframe
tagged_df.to_csv(TAGGED_ACC_EXP_FILEPATH, index=False)


# ----------------------------------------------------------------------------------- #
#                                   Get Tag Counts                                    #
# ----------------------------------------------------------------------------------- #

# Create counts of peakid and new_tag
top_tag_df = filtered_df['new_tag'].value_counts(ascending=False).reset_index()
top_tag_df = top_tag_df.iloc[:NO_TAGS_PLOT, :][['new_tag']]
tag_count_df = filtered_df.groupby(by='peakid')['new_tag'].value_counts().reset_index()
tag_count_df = top_tag_df.merge(tag_count_df, how='left', on='new_tag')

# Save exploded dataframe
tag_count_df.to_csv(TAG_COUNT_FILEPATH, index=False)
