from safelanguage.modeling.fetch_data import *


def test_delete_data():
    delete_data()
    pass


def test_download_data():
    delete_data()
    download_data(data_size='all', total_articles=2)
    pass


def test_paragraph_to_sentence_data():
    paragraph_to_sentence_data('es')
    pass

