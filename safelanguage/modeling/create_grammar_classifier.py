from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from fetch_data import paragraph_to_sentence_data, delete_sentence_data, delete_data
from sklearn.externals import joblib

# Sentence data
delete_sentence_data()
paragraph_to_sentence_data('es')


# Load training data



# data: dataset.data,
# label: dataset.target

# Creating pipeline


# wrapping classifier


# Delete data
delete_data()
