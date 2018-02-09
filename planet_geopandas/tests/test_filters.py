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


class TestLogicalFilterOperationsOnConditionFilters(object):

    def setup(self):
        self.left = RangeFilter('cloud_cover', lte=0.5)
        self.right = DateRangeFilter(field_name='published', lt=datetime.now(), gt=datetime.now() - timedelta(days=4))

    def test_and_operation_produces_and_filter(self):
        target = self.left & self.right
        assert isinstance(target, AndFilter)

    def test_or_operation_produces_and_filter(self):
        target = self.left | self.right
        assert isinstance(target, OrFilter)

    def test_not_operation_produces_and_filter(self):
        target = ~self.right
        assert isinstance(target, NotFilter)


class TestLogicalFilterOperationOnLogicalFilters(object):

    def setup(self):
        range_filter = RangeFilter('cloud_cover', lte=0.5)
        self.and_filter = AndFilter([range_filter, range_filter])
        self.or_filter = OrFilter([range_filter, range_filter])

    def test_and_operation_adds_or_to_the_existing_and_filter(self):
        target = self.and_filter & self.or_filter
        assert isinstance(target, AndFilter)
        assert target == self.and_filter

    def test_or_operation_adds_and_to_the_existing_or_filter(self):
        target = self.and_filter | self.or_filter
        assert isinstance(target, OrFilter)
        assert target != self.or_filter
