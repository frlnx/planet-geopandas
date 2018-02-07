# Planet Geopandas
Integrating geopandas with api.planet.com

##Usage

1) Sign up to the planet.com
2) Put your username and password into the environment variables `PLANET_API_USERNAME` and `PLANET_API_PASSWORD`
3) Execute the following example


    from planet_geopandas.filters import *
    from planet_geopandas.planet_api import PlanetAPI
    import geopandas as gpd
    from shapely.geometry import mapping

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.set_index('name', inplace=True)
    sweden_geojson = mapping(world.loc['Sweden', 'geometry'])
     
    api = PlanetAPI()
    filters = DateRangeFilter(field_name='published', lt=datetime.now(), gt=datetime.now() - timedelta(days=4)) and \
        RangeFilter('cloud_cover', lte=0.0) and \
        GeometryFilter(sweden_geojson)
    df = api.quick_search("test query", api.landsat_8l1g, filters)

