import geopandas
import geojson
import json
from planet_geopandas import SearchResultSerializer



class TestSearchIntegration(object):

    def setup(self):
        with open('planet_geopandas/tests/mock_data/search_response', 'r') as f:
            self.data = json.load(f)
        self.target = SearchResultSerializer()


    def test_create_dataframe(self):
        df = self.target.geodataframe(self.data)
        assert isinstance(df, geopandas.GeoDataFrame)

    def test_all_dicts_are_converted_into_more_meaningful_values(self):
        df = self.target.geodataframe(self.data)
        for column in df.columns:
            assert not df[column].apply(lambda x: isinstance(x, dict)).any(), "{} contains dicts".format(column)
