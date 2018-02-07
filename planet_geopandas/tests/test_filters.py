from planet_geopandas.filters import *
from datetime import datetime, timedelta


class TestFilterInstantiation(object):

    def test_datetime_filter(self):
        test = DateRangeFilter(field_name='published', lt=datetime.now(), gt=datetime.now() - timedelta(days=4))
        assert True