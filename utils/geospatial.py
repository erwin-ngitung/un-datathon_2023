import folium
import pandas as pd
import pycountry as pc
import geopandas as gpd
import plotly.graph_objects as go


def unit():
    units = {'oil_quantity': 'unit_x',
             'renew_quantity': 'unit_y',
             'co2_value': 'ton'}

    return units


def merge_data(df1, df2):
    data_geom = []
    data_loc = []

    for country in df1['country']:
        data_geom.append(df2[df2['country'] == country]['geometry'])
        data_loc.append(pc.countries.search_fuzzy(country)[0].alpha_3)

    df1['geometry'] = data_geom
    df1['iso_alpha'] = data_loc

    return df1


def transform_data(df1, df2):
    df1_final = df1.reset_index(drop=True)
    country = []
    year = []
    geometry = []
    loc = []

    for i, index in enumerate(df1.index.values):
        country.append(index[0])
        year.append(index[1])
        geometry.append(df2[df2['country'] == index[0]]['geometry'].values[0])
        loc.append(df2[df2['country'] == index[0]]['iso_alpha'].values[0])

    df1_final['country'] = country
    df1_final['year'] = year
    df1_final['geometry'] = geometry
    df1_final['iso_alpha'] = loc

    return df1_final


def get_plotly_map(df, df1, col_target, title):

    unit_data = unit()
    fig = go.Figure(data=go.Choropleth(
                    locations=df['iso_alpha'],
                    z=df[col_target],
                    text=df['country'],
                    colorscale='Blues',
                    autocolorscale=False,
                    reversescale=True,
                    marker_line_color='darkgray',
                    marker_line_width=0.5,
                    colorbar_title=df1[unit_data[col_target]].values[0]
    ))

    fig.update_layout(
        title_text=title,
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: UN Big Data Hackathon</a>',
            showarrow=False
        )]
    )

    return fig


def get_folium_map(df_merged, column):
    # Create a map object for choropleth map
    map_indo = folium.Map(location=[-2.49607, 117.89587],
                          tiles='OpenStreetMap',
                          zoom_start=2)

    df_shp = gpd.read_file('dataset/world_countries/World_Countries.shp').rename(columns={'COUNTRY': 'country'})

    # Set up Choropleth map object with key on Province
    folium.Choropleth(geo_data=df_shp,
                      data=df_merged,
                      columns=['country', column],
                      key_on='feature.properties.country',
                      fill_color='YlOrRd',
                      fill_opacity=1,
                      line_opacity=0.2,
                      legend_name='Ratio',
                      smooth_factor=0,
                      Highlight=True,
                      line_color='#0000',
                      name='Event',
                      show=True,
                      overlay=True
                      ).add_to(map_indo)

    # Add hover functionality
    # Style function
    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}

    # Highlight function
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    # # Create popup tooltip object
    # popup = folium.features.GeoJson(
    #         data=df_merged,
    #         style_function=style_function,
    #         control=False,
    #         highlight_function=highlight_function,
    #         tooltip=folium.features.GeoJsonTooltip(
    #             fields=['country', column],
    #             aliases=['country', column],
    #             style=('background-color: white; '
    #                    'color: #333333; font-family: arial; '
    #                    'font-size: 12px; padding: 10px;')))
    #
    # # Add tooltip object to the map
    # map_indo.add_child(popup)
    # map_indo.keep_in_front(popup)

    # Add dark and light mode
    folium.TileLayer('cartodbdark_matter',
                     name='Dark Mode',
                     control=True).add_to(map_indo)
    folium.TileLayer('cartodbpositron',
                     name='Light Mode',
                     control=True).add_to(map_indo)

    # Add a layer controller
    folium.LayerControl(collapsed=False).add_to(map_indo)

    return map_indo
