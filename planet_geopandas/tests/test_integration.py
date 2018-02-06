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