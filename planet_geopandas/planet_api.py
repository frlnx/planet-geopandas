import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
from os import getenv

from planet_geopandas.search_result_serializer import SearchResultSerializer


class PlanetAPI(object):

    _api_url_template = "https://api.planet.com/data/v1/{}"
    _quick_search_endpoint = _api_url_template.format('quick-search')

    """PlanetScope Scenes"""
    ps_scene_3band = "PSScene3Band"
    """PlanetScope Scenes"""
    ps_scene_4band = "PSScene4Band"
    """PlanetScope OrthoTiles"""
    ps_orth_tile = "PSOrthoTile"
    """RapidEye OrthoTiles"""
    re_orth_tile = "REOrthoTile"
    """RapidEye Scenes (unorthorectified strips)"""
    re_scene = "REScene"
    """SkySat Scenes"""
    sky_sat_scene = "SkySatScene"
    """Landsat8 Scenes"""
    landsat_8l1g = "Landsat8L1G"
    """Copernicus Sentinel-2 Scenes"""
    sentinel_2l1c = "Sentinel2L1C"

    headers = {
        'User-Agent': 'Python planet-geopandas lib; https://github.com/frlnx/planet-geopandas'
    }

    def __init__(self, username=None, password=None):
        if username is None:
            username = getenv("PLANET_API_USERNAME")
            password = getenv("PLANET_API_PASSWORD")
        if password is None:
            password = getpass()
        self.auth = HTTPBasicAuth(username, password)

    def quick_search(self, name, item_types, filters, max_results=250):
        assert 1 <= len(name) <= 64
        if isinstance(item_types, str):
            item_types = [item_types]
        query = {
            "name": name,
            "item_types": item_types,
            "filter": filters.to_dict()
        }
        response = requests.post(self._quick_search_endpoint, json=query, auth=self.auth, headers=self.headers)
        assert response.status_code == 200, response.content
        response_data = response.json()
        serializer = SearchResultSerializer()
        df = serializer.geodataframe(response_data)
        return df