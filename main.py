from gensim.models import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser
# from openai import OpenAI
from transformers import pipeline
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora
import nltk
# import time
# import csv
import os

# ----------------------------------------------------------------------------------- #
#                                  Define constants                                   #
# ----------------------------------------------------------------------------------- #

# Input filepaths
EXP_FILEPATH = os.path.join('data', 'input', 'expeditions.csv')

# Output filepaths
TAGGED_ACC_FILEPATH = os.path.join('data', 'output', 'tagged_accidents.csv')
TAG_FILEPATH = os.path.join('data', 'input', 'tag_df.tsv')
ACCIDENT_FILEPATH = os.path.join('data', 'output', 'acc_df.csv')

# Other
NO_PEAKS = 10  # Number of peaks to plot
RESET_ACC_DF = True
nltk.download('stopwords')
nltk.download('punkt')

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
key_df.sort_values(by='expid', ascending=False, inplace=True, ignore_index=True)
key_df = key_df.iloc[:NO_PEAKS, :]
acc_df = key_df[['peakid']].merge(exp_df[['peakid', 'accidents']], how='left', on='peakid')
acc_df.dropna(subset=['accidents'], inplace=True, ignore_index=True)

# # Save acc_df (one time only)
# acc_df.reset_index(inplace=True)
# acc_df.rename(columns={'index': 'acc_id'}, inplace=True)
# acc_df.to_csv(ACCIDENT_FILEPATH, index=False)

# ----------------------------------------------------------------------------------- #
#                                      Find Topics                                    #
# ----------------------------------------------------------------------------------- #

# Sample text data
text = ' '.join([ele for ele in acc_df.accidents])

# Tokenization and removing stop words
stop_words = set(stopwords.words('english'))
tokens = word_tokenize(text.lower())
tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

# Create bigrams
bigram_model = Phrases([tokens], min_count=5, threshold=100)
bigram_phraser = Phraser(bigram_model)
bigram_tokens = list(bigram_phraser[tokens])

# Create a Gensim dictionary and corpus with bigrams
dictionary = corpora.Dictionary([bigram_tokens])
corpus = [dictionary.doc2bow(bigram_tokens)]

# Train the LDA model
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=10)

# Print the identified topics
topics = lda_model.print_topics()
for topic in topics:
    print(topic)


# ----------------------------------------------------------------------------------- #
#                                 Initial Data Processing                             #
# ----------------------------------------------------------------------------------- #

#
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# sequence_to_classify = "one day I will see the world"
# candidate_labels = ['travel', 'cooking', 'dancing']
#
# result = classifier(sequence_to_classify, candidate_labels)
# print(result)

print('end')


