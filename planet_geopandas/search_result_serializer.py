import geopandas
from shapely.geometry import shape


class SearchResultSerializer(object):
    perms = ['assets.analytic_xml:download',
             'assets.basic_analytic_dn:download',
             'assets.basic_analytic_dn_xml:download',
             'assets.basic_analytic_xml:download',
             'assets.analytic_dn:download',
             'assets.basic_udm:download',
             'assets.analytic:download',
             'assets.visual:download',
             'assets.analytic_dn_xml:download',
             'assets.basic_analytic_rpc:download',
             'assets.basic_analytic_dn_rpc:download',
             'assets.visual_xml:download',
             'assets.basic_analytic:download',
             'assets.udm:download']

    def __init__(self):
        self.df = geopandas.GeoDataFrame()

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
        permission_df = geopandas.GeoDataFrame(df['_permissions'].apply(self._permission_dict).tolist())
        df.merge(permission_df, left_index=True, right_index=True)
        del df['_permissions']
        df['geometry'] = df['geometry'].apply(shape)
        df['properties.acquired'] = geopandas.pd.to_datetime(df['properties.acquired'])
        df['properties.published'] = geopandas.pd.to_datetime(df['properties.published'])
        df['properties.updated'] = geopandas.pd.to_datetime(df['properties.updated'])
        return df

    def _permission_dict(self, permission_list):
        return {perm: perm in permission_list for perm in self.perms}

    @property
    def row_count(self):
        return len(self.df)

    def ingest(self, data: dict):
        features = data['features']
        if len(features) == 0:
            raise AttributeError("No lines given")
        df = geopandas.GeoDataFrame(data['features'])
        self.clean(df)
        self.df = self.df.append(df)

    def geodataframe(self):
        return self.df.reset_index(drop=True)
