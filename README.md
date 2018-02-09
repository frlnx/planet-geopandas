# Planet Geopandas
Integrating geopandas with api.planet.com

## Usage

1) Sign up on planet.com
2) Put your username and password into the environment variables `PLANET_API_USERNAME` and `PLANET_API_PASSWORD`
3) Execute the following example


    from planet_geopandas.filters import *
    from planet_geopandas import PlanetAPI
    import geopandas as gpd
    from datetime import datetime, timedelta

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.set_index('name', inplace=True)
    
    api = PlanetAPI()
    filters = DateRangeFilter(field_name='published', lt=datetime.now(), gt=datetime.now() - timedelta(days=1)) & \
        RangeFilter('cloud_cover', lte=0.1, gte=0.01) & \
        GeometryFilter.from_geopandas(world.loc[['Sweden', 'Norway'], 'geometry'])
    df = api.quick_search("test query", api.landsat_8l1g, filters, max_results=500)

### To visualize data, you could then do something like this:

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.set_aspect('equal')

    df.plot(ax=ax, column='properties.usable_data', alpha=0.4)
    world.loc[['Sweden', 'Norway']].plot(ax=ax, color='None', edgecolor='black')

    plt.show()
