from shapely.geometry import mapping
from functools import reduce


class Filter(object):
    def __init__(self, conditions):
        self.conditions = conditions


class ConditionFilter(object):
    def __init__(self, field_name, config):
        self.field_name = field_name
        self.config = config

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "field_name": self.field_name,
            "config": self.config
        }

    def __and__(self, other):
        if isinstance(other, AndFilter):
            other.conditions.append(self)
            return other
        return AndFilter([self, other])

    def __or__(self, other):
        if isinstance(other, OrFilter):
            other.conditions.append(self)
            return other
        return OrFilter([self, other])

    def __invert__(self):
        return NotFilter(self)


class DateRangeFilter(ConditionFilter):
    """Matches dates that fall within a range."""

    def __init__(self, field_name, gt=None, gte=None, lt=None, lte=None, timezone="Z"):
        assert field_name in ['acquired', 'published', 'updated']
        assert not (lt and lte), "lt and lte are mutually exclusive"
        assert not (gt and gte), "gt and gte are mutually exclusive"
        config = {"gt": gt, "gte": gte, "lt": lt, "lte": lte}
        for key in list(config.keys()):
            val = config[key]
            if not val:
                del config[key]
                continue
            config[key] = config[key].isoformat() + timezone
        super().__init__(field_name, config)


class GeometryFilter(ConditionFilter):
    """Matches using GeoJSON geometry."""

    def __init__(self, geometry):
        assert geometry['type'] in ["Polygon", "MultiPolygon", "Feature", "FeatureCollection"]
        if geometry['type'] in ['Polygon', 'MultiPolygon']:
            assert isinstance(geometry['coordinates'], list) or isinstance(geometry['coordinates'], tuple)
        else:
            assert isinstance(geometry['features'], list) or isinstance(geometry['features'], tuple)
        super().__init__("geometry", geometry)

    @classmethod
    def from_geopandas(cls, geopandas_df):
        return cls({
            'type': 'MultiPolygon', 'coordinates':
            reduce(lambda x, y: x + y, map(cls._multi_polygonize, geopandas_df.geometry.apply(mapping).tolist()))
        })

    @staticmethod
    def _multi_polygonize(d):
        if d['type'] == "MultiPolygon":
            return d['coordinates']
        else:
            return [d['coordinates']]


class NumberInFilter(ConditionFilter):
    """Matches any number within the array of provided numbers."""

    def __init__(self, field_name, value_list):
        assert field_name in ["sun_azimuth", "sun_elevation", "gsd", "view_angle", "cloud_cover", "black_fill",
                              "usable_data", "origin_y"]
        assert isinstance(value_list, list)
        super().__init__(field_name, value_list)


class RangeFilter(ConditionFilter):
    """Matches numbers that fall within a range."""

    def __init__(self, field_name, gt=None, gte=None, lt=None, lte=None):
        assert field_name in ["sun_azimuth", "sun_elevation", "gsd", "view_angle", "cloud_cover", "black_fill",
                              "usable_data", "origin_y"]
        assert not (lt and lte), "lt and lte are mutually exclusive"
        assert not (gt and gte), "gt and gte are mutually exclusive"
        config = {"gt": gt, "gte": gte, "lt": lt, "lte": lte}
        for key in list(config.keys()):
            val = config[key]
            if val is None:
                del config[key]

        upper_bound = config.get('lt', config.get('lte', float('inf')))
        lower_bound = config.get('gt', config.get('gte', float('-inf')))
        assert upper_bound >= lower_bound, "lower_bound > upper_bound"
        assert len(config) > 0, "Need at least one value in the RangeFilter"
        super().__init__(field_name, config)


class StringInFilter(ConditionFilter):
    """Matches any string within the array of provided strings."""

    def __init__(self, field_name, string_list):
        assert field_name in ["catalog_id", "strip_id", "item_type", "grid_cell",
                              "satellite_id", "provider", "ground_control"]
        assert isinstance(string_list, list)
        super().__init__(field_name, string_list)


class LogicalFilter(Filter):
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "config": [condition.to_dict() for condition in self.conditions]
        }

    def __and__(self, other):
        self.conditions.append(other)
        return self

    def __or__(self, other):
        if isinstance(other, ConditionFilter):
            self.conditions.append(other)
            return other
        return OrFilter([self, other])

    def __invert__(self):
        return NotFilter(self)


class AndFilter(LogicalFilter):
    pass

class OrFilter(LogicalFilter):
    pass

class NotFilter(LogicalFilter):
    pass
