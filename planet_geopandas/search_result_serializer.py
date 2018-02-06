import geopandas
from shapely.geometry import shape


class SearchResultSerializer(object):

    def __init__(self):
        pass

    def clean(self, df: geopandas.GeoDataFrame):
        unpack = {
            '_links': ['thumbnail', '_self', 'assets'],
            'properties': ['catalog_id', 'anomalous_pixels', 'sun_azimuth', 'acquired', 'published', 'sun_elevation',
                           'gsd', 'strip_id', 'pixel_resolution', 'item_type', 'origin_x', 'grid_cell', 'updated',
                           'view_angle', 'satellite_id', 'cloud_cover', 'rows', 'provider', 'black_fill',
                           'ground_control', 'epsg_code', 'usable_data', 'columns', 'origin_y']
        }
        for column, fields in unpack.items():
            for field in fields:
                namespaced_column = "{}.{}".format(column, field)
                df[namespaced_column] = df[column].apply(lambda x: x.get(field))
            del df[column]
        df['geometry'] = df['geometry'].apply(shape)
        return df

    def geodataframe(self, data: dict):
        df = geopandas.GeoDataFrame(data['features'])
        self.clean(df)
        return df
