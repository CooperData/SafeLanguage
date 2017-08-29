from safelanguage.modeling.fetch_data import *


class TestResourceHandler(object):

    def test_download_all_data(self):
        delete_data()
        download_all_data()
        pass
