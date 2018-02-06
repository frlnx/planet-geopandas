import geopandas


class SearchResultSerializer(object):

    def __init__(self):
        pass

    def geodataframe(self, data: dict):
        return geopandas.GeoDataFrame(data['features'])
