from concurrent.futures import ProcessPoolExecutor, as_completed
from transformers import pipeline
import pandas as pd
import logging
import time
import os


# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

# Input filepaths
EXP_FILEPATH = os.path.join('data', 'input', 'expeditions.csv')
CAT_FILEPATH = os.path.join('data', 'input', 'labels.csv')

# Output filepaths
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'accident_reports.csv')
LABELS_FILEPATH = os.path.join('data', 'input', 'labels.csv')
TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')

# Other
NO_PEAKS = 5  # Number of peaks to plot
GENERATE_ACCIDENTS = False
LABEL_THRESHOLD = 0.8
ORIG_LOG_CONFIG = logging.getLogger().getEffectiveLevel()


# ----------------------------------------------------------------------------------- #
#                                   Configurations                                    #
# ----------------------------------------------------------------------------------- #

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------- #
#                                        Get Tags                                     #
# ----------------------------------------------------------------------------------- #

# Load accident descriptions
acc_df = pd.read_csv(ACCIDENT_FILEPATH)

# Load labels
lab_df = pd.read_csv(LABELS_FILEPATH)
candidate_labels = lab_df.label.values

# Instantiate classification pipeline
logging.getLogger("transformers").setLevel(logging.ERROR)  # Temporarily set warnings to ERROR only
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def classify_sequence(row):
    """Function for classifying an accident description as described in row['accidents']."""

    result = classifier(row['accidents'], candidate_labels, multi_label=True)
    filtered_labels = [label for label, score in zip(result['labels'], result['scores']) if score >= LABEL_THRESHOLD]

    return row['acc_id'], filtered_labels


if __name__ == "__main__":

    num_workers = 6
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(classify_sequence, this_row) for _, this_row in acc_df.iloc[:10].iterrows()]
        results = [future.result() for future in as_completed(futures)]

    res_df = pd.DataFrame(results, columns=['acc_id', 'tags'])
    res_df.sort_values(by='acc_id', ascending=True, inplace=True)
    res_df.to_csv(TAGGED_ACC_FILEPATH, index=False)

    logging.basicConfig(level=ORIG_LOG_CONFIG)
