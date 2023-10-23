import gpxpy

import pandas    as pd
import streamlit as st

from gpxpy import gpx
from GPXFunctions import GPXObject

# We configure Streamlit WebApp. 
st.set_page_config(page_title='Map Tracker', page_icon='📊')
st.title('Fake Strava')

def Main():
    
    file = st.file_uploader('Choose the GPX file.', type=['gpx'])
    if file:
        typeOfMap = st.radio('How do you want to visualize your map?',['Normal Map','Elevation Map'])
        gpxInfo = GPXObject(file)
        route_info = gpxInfo.readGPXFile()
        if typeOfMap == 'Elevation Map':
            route_infoColors = gpxInfo.calculateElevationColors()
            st.map(route_infoColors,color='colors',size=2)
            st.line_chart(route_info['elevation'])
        elif typeOfMap == 'Normal Map':
            st.map(route_info,size=2)
    else:
        st.map()

Main()