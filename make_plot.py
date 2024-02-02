from pyllplot import SortedStream
import pandas as pd
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

# TAG_COUNT_FILEPATH = os.path.join('data', 'output', 'tag_count.csv')
PEAK_FILEPATH = os.path.join('data', 'input', 'peaks.csv')
PLOT_FILEPATH = os.path.join('data', 'output', 'sorted_stream.svg')
NO_EXPED_FILEPATH = os.path.join('data', 'output', 'no_exped.csv')
TAGGED_ACC_FIN_FILEPATH = os.path.join('data', 'output', 'tagged_accidents_final.csv')

# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------- #
#                                      Load Data                                      #
# ----------------------------------------------------------------------------------- #

# Create tag counts by peak
tagged_df = pd.read_csv(TAGGED_ACC_FIN_FILEPATH)
tag_count_df = tagged_df.groupby('peakid')['new_tag'].value_counts().reset_index()

# Scale count by proportion of expeditions for peak
exped_ct_df = pd.read_csv(NO_EXPED_FILEPATH)
tag_count_df = tag_count_df.merge(exped_ct_df, how='left', on='peakid')
tag_count_df['count_frac'] = tag_count_df['count'] / tag_count_df['no_exped']

# Make sorted stream graph
sorted_stream = SortedStream(
    tag_count_df,
    x_col="new_tag",
    height_col="count_frac",
    label_col="peakid",
    pad=0.0,
    centered=True,
    ascending=True,
)
# color_palette = ["#fb6207", "#fba981",
#                  "#ca0203", "#ead8da",
#                  "#ca0203", "#ead8da",
#                  "#131220", "#54658b",
#                  "#f2b202", "#f7dfaf",
#                  "#01a0e6", "#48c8f6",
#                  ]

color_palette = ["#ca0203", "#131220", "#ead8da", "#f2b202", "#48c8f6"]
sorted_stream.plot(filepath=PLOT_FILEPATH, color_palette=color_palette, title=None, figsize=(14, 6))
