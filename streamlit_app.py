import streamlit as st 
import geopandas as gpd
import requests
import geojson
import pygwalker as pyg
from pyproj import CRS
from owslib.wfs import WebFeatureService

url = "https://portal.csdi.gov.hk/server/services/common/cedd_rcd_1640249280153_17521/MapServer/WFSServer"

query_params = dict(
    service="WFS",
    version="2.0.0",
    request="GetFeature",
    typeName="esri:Incident",
    outputFormat="GEOJSON",
)

def load_data(nrows):
    # Fetch data from WFS using requests
    query_params['resultREcordCount'] = nrows
    r = requests.get(url, params=query_params)
    data = gpd.GeoDataFrame.from_features(geojson.loads(r.content), crs="EPSG:4326") 
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(500)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.title("Connect to CSDI") 
st.subheader("Find slope data") 
st.write("Show it, show it✨ ")
st.write( '### 1. Dataset Preview ')
# st.dataframe(data) This causes error because st.dataframe cannot handle geometry in geopandas
walker = pyg.walk(data)