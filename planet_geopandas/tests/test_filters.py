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


class TestRangeFilter(object):

    def setup(self):
        self.target = RangeFilter('cloud_cover', lte=0.0)

    def test_range_filter_asserts_less_than_or_equal_to_zero_cloud_cover(self):
        assert self.target.to_dict() == {'type': 'RangeFilter', 'field_name': 'cloud_cover', 'config': {'lte': 0.0}}
