import streamlit as st 
import geopandas as gpd
import pandas as pd
import requests
import geojson
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
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

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Showing landslide data from cSDI",
    layout="wide"
)

def load_data(nrows):
    # Fetch data from WFS using requests
    query_params['resultRecordCount'] = nrows
    r = requests.get(url, params=query_params)
    data = gpd.GeoDataFrame.from_features(geojson.loads(r.content), crs="EPSG:4326") 
    data['longitude']=data['geometry'].x
    data['latitude']=data['geometry'].y
    data = data.drop(columns='geometry')
    return data

# Establish communication between pygwalker and streamlit
init_streamlit_comm()
 
# Add a title
st.title("Loading Pygwalker In Streamlit")

# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
   # Create a text element and let the reader know the data is loading.
    st.text('Loading data...')
    
    df = load_data(5000)
    # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
    # Notify the reader that the data was successfully loaded.
    st.text('Loading data...done!')
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
 
renderer = get_pyg_renderer()

tab1, tab2 = st.tabs(
    ["graphic walker", "data profiling"]
)

with tab1:
    # Render your data exploration interface. Developers can use it to build charts by drag and drop.
    renderer.render_explore()

with tab2:
    renderer.explorer(default_tab="data")