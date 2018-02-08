import geopandas
import json
from planet_geopandas import SearchResultSerializer


class TestSearchIntegration(object):

    def setup(self):
        with open('planet_geopandas/tests/mock_data/search_response', 'r') as f:
            self.data = json.load(f)
        self.target = SearchResultSerializer()

    def test_create_dataframe(self):
        self.target.ingest(self.data)
        df = self.target.geodataframe()

        assert isinstance(df, geopandas.GeoDataFrame)

    def test_all_dicts_are_converted_into_more_meaningful_values(self):
        self.target.ingest(self.data)
        df = self.target.geodataframe()

        for column in df.columns:
            try:
                keys = df.loc[0, column].keys()
            except AttributeError:
                keys = "Could not find keys!"
            assert not df[column].apply(lambda x: isinstance(x, dict)).any(),\
                "{} contains dicts with keys {}".format(column, keys)

    def test_geometry_is_a_geoseries(self):
        self.target.ingest(self.data)
        df = self.target.geodataframe()

        assert isinstance(df.geometry, geopandas.GeoSeries)

    def test_geometies_are_polygons(self):
        self.target.ingest(self.data)
        df = self.target.geodataframe()

        assert (df.geometry.geom_type == "Polygon").all()

    def test_country_of_search_response(self):
        self.target.ingest(self.data)
        df = self.target.geodataframe()

        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        countries = geopandas.sjoin(df, world, how="inner", op='intersects')
        assert (countries['name'] == 'United States').all()
