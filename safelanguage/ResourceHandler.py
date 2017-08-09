from sklearn.externals import joblib


class ResourceHandler:

    RESOURCE_PATH = './safelanguage/resources/'
    MODEL_INDEX = 0
    TARGET_INDEX = 1

    def get_language_classifier(self):
        language_classifier = joblib.load(self.RESOURCE_PATH + 'language_classification_model.pkl')
        return language_classifier[self.MODEL_INDEX], language_classifier[self.TARGET_INDEX]



