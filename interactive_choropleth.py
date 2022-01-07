# -*- coding: utf-8 -*-
"""QM2 - Interactive Choropleth actual.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-qiqRGETi4q1AyL1knv_ywmW-Ypg8RLs
"""

!pip install geopandas
!pip install pysal

import folium as fm
import pandas as pd
import geopandas as gp

#giving the notebook access to google drive, where all relevant datasets and files are hosted
from google.colab import drive
drive.mount('/content/drive')

#dataset with shapefile data for each borough
data_path = "./drive/MyDrive/QM2_Choropleth/LondonBorough.json"

boroughGeodata = gp.read_file(data_path)

#removing data for City of London, as other datasets don't include it, since the City is technically not a borough
boroughGeodataNoCity = boroughGeodata.drop(32)

boroughGeodataNoCity['name'] = boroughGeodataNoCity['name'].astype('str')

boroughGeodataNoCity.tail()

#using folium to create the map on which we can create the choropleth
m_crime = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_crime)

#violent crime dataset
data_path = "./drive/MyDrive/QM2_Choropleth/Violent Crimes per Borough.csv"
violentcrime = pd.read_csv(data_path, encoding = 'latin1')
violentcrime.head()

#merging the violent crime dataset on the shapefile dataset
geocrime = pd.merge(boroughGeodataNoCity, violentcrime, left_on='code', right_on ='GSS_CODE')
geocrime.head()

#creating the choropleth for violent crime using folium
m_crime.choropleth(
    geo_data = geocrime,
    name = "choropleth",
    data = geocrime,
    columns = ["name", "AVERAGE VIOLENT CRIMES PER 1000 PEOPLE"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Violent crimes (per 1000 people)",
    smooth_factor = 0)

#now creating a tooltip that shows the borough and relevant stats when you hover over it
style_function = lambda x: {"fillColor": "#ffffff", 
                            "color":"#000000", 
                            "fillOpacity": 0.1, 
                            "weight": 0.1}
highlight_function = lambda x: {"fillColor": "#000000", 
                                "color":"#000000", 
                                "fillOpacity": 0.50, 
                                "weight": 0.1}

interactive_tooltip_crime = fm.features.GeoJson(
    geocrime,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","AVERAGE VIOLENT CRIMES PER 1000 PEOPLE"],
        aliases = ["Borough: ","Violent crimes (per 1000 people)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_crime.add_child(interactive_tooltip_crime)
m_crime.keep_in_front(interactive_tooltip_crime)
fm.LayerControl().add_to(m_crime)

#the choropleth, with interactive tooltip, has been placed onto the map

#repeating the process for other factors: police strength, number of stop and searches, etc. Police strength first

m_police = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_police)

data_path = "./drive/MyDrive/QM2_Choropleth/Police Strength per Borough.csv"
police_strength = pd.read_csv(data_path, encoding = 'latin1')

geopolice = pd.merge(boroughGeodataNoCity, police_strength, left_on='code', right_on ='GSS_CODE')

m_police.choropleth(
    geo_data = geopolice,
    name = "choropleth",
    data = geopolice,
    columns = ["name", "Officers per 1000 average"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Police officers (per 1000 people)",
    smooth_factor = 0)

interactive_tooltip_police_strength = fm.features.GeoJson(
    geopolice,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","Officers per 1000 average"],
        aliases = ["Borough: ","Police officers (per 1000 people)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_police.add_child(interactive_tooltip_police_strength)
m_police.keep_in_front(interactive_tooltip_police_strength)
fm.LayerControl().add_to(m_police)

#creating choropleth for income

m_income = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_income)

data_path = "./drive/MyDrive/QM2_Choropleth/Income per Borough.csv"
income = pd.read_csv(data_path, encoding = 'latin1')

geoincome = pd.merge(boroughGeodataNoCity, income, left_on='code', right_on ='Code')
geoincome.head()

m_income.choropleth(
    geo_data = geoincome,
    name = "choropleth",
    data = geoincome,
    columns = ["name", "Average Income (2011-2018)"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Average income per week (£)",
    smooth_factor = 0)

interactive_tooltip_income = fm.features.GeoJson(
    geoincome,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","Average Income (2011-2018)"],
        aliases = ["Borough: ","Average income per week (£)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_income.add_child(interactive_tooltip_income)
m_income.keep_in_front(interactive_tooltip_income)
fm.LayerControl().add_to(m_income)

#creating choropleth for nightlife

m_nightlife = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_nightlife)

data_path = "./drive/MyDrive/QM2_Choropleth/Pubs and Clubs per Borough.csv"
nightlife = pd.read_csv(data_path, encoding = 'latin1')

geonightlife = pd.merge(boroughGeodataNoCity, nightlife, left_on='code', right_on ='Code')
geonightlife.head()

#creating the choropleth for age using features from the folium library
m_nightlife.choropleth(
    geo_data = geonightlife,
    name = "choropleth",
    data = geonightlife,
    columns = ["name", "Average pubs and clubs 2011-2018"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Pubs and clubs (per 1000 people)",
    smooth_factor = 0)

interactive_tooltip_nightlife = fm.features.GeoJson(
    geonightlife,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","Average pubs and clubs 2011-2018"],
        aliases = ["Borough: ","Pubs and clubs (per 1000 people)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_nightlife.add_child(interactive_tooltip_nightlife)
m_nightlife.keep_in_front(interactive_tooltip_nightlife)
fm.LayerControl().add_to(m_nightlife)

#creating choropleth for happiness

m_happiness = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_happiness)

data_path = "./drive/MyDrive/QM2_Choropleth/Happiness per Borough.csv"
happiness = pd.read_csv(data_path, encoding = 'latin1')

geohappiness = pd.merge(boroughGeodataNoCity, happiness, left_on='code', right_on ='Code')
geohappiness.head()

m_happiness.choropleth(
    geo_data = geohappiness,
    name = "choropleth",
    data = geohappiness,
    columns = ["name", "Average Happiness"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Happiness (scale of 1 - 10)",
    smooth_factor = 0)

interactive_tooltip_happiness = fm.features.GeoJson(
    geohappiness,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","Average Happiness"],
        aliases = ["Borough: ","Happiness (scale of 1 - 10)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_happiness.add_child(interactive_tooltip_happiness)
m_happiness.keep_in_front(interactive_tooltip_happiness)
fm.LayerControl().add_to(m_happiness)

#creating choropleth for stop and search

m_stopandsearch = fm.Map(location=[51.5074, 0], zoom_start=9.5,tiles=None)
fm.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m_stopandsearch)

data_path = "./drive/MyDrive/QM2_Choropleth/Stop and Search per Borough.csv"
stopandsearch = pd.read_csv(data_path, encoding = 'latin1')

geostopandsearch = pd.merge(boroughGeodataNoCity, stopandsearch, left_on='code', right_on ='Code')
geostopandsearch.head()

m_stopandsearch.choropleth(
    geo_data = geostopandsearch,
    name = "choropleth",
    data = geostopandsearch,
    columns = ["name", "Average Stop and Search"],
    key_on = "feature.properties.name",
    fill_color = "YlGn",
    fill_opacity = 2,
    line_opacity = 1,
    legend_name = "Stop and searches performed (per 1000 people)",
    smooth_factor = 0)

interactive_tooltip_stopandsearch = fm.features.GeoJson(
    geostopandsearch,
    style_function = style_function, 
    control = False,
    highlight_function = highlight_function, 
    tooltip = fm.features.GeoJsonTooltip(
        fields = ["name","Average Stop and Search"],
        aliases = ["Borough: ","Stop and searches performed (per 1000 people)"],
        style = ("background-color: white; color: #; font-family: arial; font-size: 12px;") 
    )
)
m_stopandsearch.add_child(interactive_tooltip_stopandsearch)
m_stopandsearch.keep_in_front(interactive_tooltip_stopandsearch)
fm.LayerControl().add_to(m_stopandsearch)

#saving all the choropleths as html files to place onto the website
m_crime.save("./drive/MyDrive/QM2_Choropleth/crime_choropleth.html")
m_stopandsearch.save("./drive/MyDrive/QM2_Choropleth/stopandsearch_choropleth.html")
m_happiness.save("./drive/MyDrive/QM2_Choropleth/happiness_choropleth.html")
m_income.save("./drive/MyDrive/QM2_Choropleth/income_choropleth.html")
m_police.save("./drive/MyDrive/QM2_Choropleth/police_choropleth.html")
m_nightlife.save("./drive/MyDrive/QM2_Choropleth/nightlife_choropleth.html")

