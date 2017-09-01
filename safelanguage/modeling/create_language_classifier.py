from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from fetch_data import download_data, delete_data
from sklearn.externals import joblib

# Download data
delete_data()
download_data(data_size='all')


# Load training data
languages_data_folder = './modeling//data/paragraphs'
dataset = load_files(languages_data_folder)

print(dataset)
print(dataset.target_names)

# data: dataset.data,
# label: dataset.target

# Creating pipeline
hashing_vectorizer = HashingVectorizer(analyzer='char_wb', ngram_range=(1, 3))
text_clf = Pipeline([
                    ('vec', hashing_vectorizer),
                    ('clf', Perceptron()),
                    ])

clf = text_clf.fit(dataset.data, dataset.target)
clf_model = [clf, dataset.target_names]

# wrapping classifier
joblib.dump(clf_model, './resources/language_classification_model.pkl')

# Delete data
delete_data()
