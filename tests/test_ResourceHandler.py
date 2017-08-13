from safelanguage.ResourceHandler import ResourceHandler


class TestResourceHandler(object):

    def test_get_language_classifier(self):
        sentence = ['Esto es una oracion en español y deberia ser predecido como es']
        resource_handler = ResourceHandler()
        clf, target_names = resource_handler.get_language_classifier()
        prediction = clf.predict(sentence)
        assert target_names[prediction[0]] == 'es'

