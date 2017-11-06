from safelanguage.modeling.fetch_data import *


class TestResourceHandler(object):

    def test_download_data(self):
        delete_data()
        download_data(data_size='all')
        pass
