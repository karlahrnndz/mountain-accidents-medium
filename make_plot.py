from pyllplot import SortedStream
import pandas as pd
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

TAG_COUNT_FILEPATH = os.path.join('data', 'output', 'tag_count.csv')
PEAK_FILEPATH = os.path.join('data', 'input', 'peaks.csv')
PLOT_FILEPATH = os.path.join('data', 'output', 'sorted_stream.svg')
NO_EXPED_FILEPATH = os.path.join('data', 'output', 'no_exped.csv')


# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------- #
#                                      Load Data                                      #
# ----------------------------------------------------------------------------------- #

tag_count_df = pd.read_csv(TAG_COUNT_FILEPATH)
peak_df = pd.read_csv(PEAK_FILEPATH)

tag_count_df = tag_count_df.merge(peak_df[['peakid', 'heightm']], how='left', on='peakid')
tag_count_df['x'] = tag_count_df['heightm'].astype('str') + '_' + tag_count_df['peakid']

exped_ct_df = pd.read_csv(NO_EXPED_FILEPATH)
tag_count_df = tag_count_df.merge(exped_ct_df, how='left', on='peakid')

tag_count_df['count_frac'] = tag_count_df['count'] / tag_count_df['no_exped']

sorted_stream = SortedStream(
    tag_count_df,
    x_col="x",
    height_col="count_frac",
    label_col="new_tag",
    pad=0.0,
    centered=True,
    ascending=True,
)
color_palette = ["#fb6207", "#fba981",
                 "#ca0203", "#ead8da",
                 "#131220", "#54658b",
                 "#f2b202", "#f7dfaf",
                 "#01a0e6", "#48c8f6",
                 ]
sorted_stream.plot(filepath=PLOT_FILEPATH, color_palette=color_palette, title=None, figsize=None)

# sorted_stream = SortedStream(
#     tag_count_df,
#     x_col="new_tag",
#     height_col="count_frac",
#     label_col="peakid",
#     pad=0.0,
#     centered=True,
#     ascending=True,
# )
# color_palette = ["#fb6207", "#fba981",
#                  "#ca0203", "#ead8da",
#                  "#131220", "#54658b",
#                  "#f2b202", "#f7dfaf",
#                  "#01a0e6", "#48c8f6",
#                  ]
# sorted_stream.plot(filepath=PLOT_FILEPATH, color_palette=None, title=None, figsize=None)

