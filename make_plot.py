import matplotlib.pyplot as plt
import pandas as pd
import json
import os


from pyllplot import SortedStream
import pandas as pd
import os

FILEPATH = os.path.join("..", "output", "text.svg")

# data = pd.DataFrame(
#     {
#         "my_x": [1, 2, 3, 4, 1, 2, 3, 4],
#         "my_height": [3, 3, 1, 3, 2, 2, 2, 2],
#         "my_label": ["a", "a", "a", "a", "b", "b", "b", "b"],
#     }
# )

# data = pd.DataFrame(
#     {
#         "my_x": pd.to_datetime(['2022-01-01 12:00:00', '2022-01-01 14:30:00',
#                                 '2022-01-03 16:45:00', '2022-01-04 18:20:00',
#                                 '2022-01-01 12:00:00', '2022-01-01 14:30:00',
#                                 '2022-01-03 16:45:00', '2022-01-04 18:20:00']),
#         "my_height": [3, 3, 1, 3, 2, 2, 2, 2],
#         "my_label": ["a", "a", "a", "a", "b", "b", "b", "b"],
#     }
# )

data = pd.DataFrame(
    {
        "my_x": [
            "2022-01-01",
            "2022-01-02",
            "2022-01-03",
            "2022-01-04",
            "2022-01-01",
            "2022-01-02",
            "2022-01-03",
            "2022-01-04",
        ],
        "my_height": [1, 2, 3, 1, 2, 1, 4, 0.5],
        "my_label": ["a", "a", "a", "a", "b", "b", "b", "b"],
    }
)

sorted_stream = SortedStream(
    data,
    x_col="my_x",
    height_col="my_height",
    label_col="my_label",
    pad=0.05,
    centered=True,
    ascending=True,
)
sorted_stream.plot(filepath=None, color_palette=None, title=None, figsize=None)
