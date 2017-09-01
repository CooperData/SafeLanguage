from sklearn.externals import joblib
import pickle


class ResourceHandler:

    RESOURCE_PATH = './resources/'
    MODEL_INDEX = 0
    TARGET_INDEX = 1

    def get_language_classifier(self):
        language_classifier = self._extract_file('language_classification_model.pkl')
        return language_classifier[self.MODEL_INDEX], language_classifier[self.TARGET_INDEX]

    def get_feature_pages(self):
        feature_articles = self._extract_file('featured_links.pkl')
        return feature_articles

    def _extract_file(self, file):
        try:
            unpickled_file = joblib.load(self.RESOURCE_PATH + file)
            return unpickled_file
        except (OSError, IOError) as e:
            print('file not found')

