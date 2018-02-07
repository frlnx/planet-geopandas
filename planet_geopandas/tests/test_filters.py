from planet_geopandas.filters import *
from datetime import datetime, timedelta


class TestFilterInstantiation(object):

    def test_datetime_filter(self):
        DateRangeFilter(field_name='published', lt=datetime.now(), gt=datetime.now() - timedelta(days=4))
        assert True

    def test_range_filter(self):
        RangeFilter('cloud_cover', lte=0.0)
        assert True

    def test_geometry_filter(self):
        geometry = {"type": "Polygon", "coordinates": [[-1, -1], [1, -1], [1, 1], [-1, 1]]}
        GeometryFilter(geometry)
        assert True
