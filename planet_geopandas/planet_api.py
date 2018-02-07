import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
from os import getenv


class PlanetAPI(object):

    _api_url_template = "https://api.planet.com/data/v1/{}"
    _quick_search_endpoint = _api_url_template.format('quick-search')

    def __init__(self, username=None, password=None):
        if username is None:
            username = getenv("PLANET_API_USERNAME")
            password = getenv("PLANET_API_PASSWORD")
        if password is None:
            password = getpass()
        self.auth = HTTPBasicAuth(username, password)

    def quick_search(self, item_types, filters):
        query = {
            "name": "",
            "item_types": item_types,
            "filter": filters.to_dict()
        }
        response = requests.post(self._quick_search_endpoint, json=query)