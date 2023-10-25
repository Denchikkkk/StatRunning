import gpxpy

import pandas    as pd
import streamlit as st

from gpxpy        import gpx
from GPXFunctions import GPXObject

# We configure Streamlit WebApp. 
st.set_page_config(page_title='Map Tracker', page_icon='📊')
st.title('Fake Strava')

def Main():
    file = st.file_uploader('Choose the GPX file.', type=['gpx'])

    if file:
        typeOfMap  = st.radio('How do you want to visualize your map?',['Normal Map','Elevation Map'])
        gpxInfo    = GPXObject(file)
        route_info = gpxInfo.readGPXFile()

        if typeOfMap == 'Elevation Map':
            route_infoColors = gpxInfo.calculateElevationColors()

            # Map plot. The points will draw the segment done. 
            st.map(route_infoColors,color='colors',size=2)

            # Line Chart Plot. X-axis = Distance (in KM.) Y-axis = Height (respective to the level of the sea.)
            chart_data = route_info[['distance','elevation']].set_index('distance')
            st.line_chart(chart_data)

        elif typeOfMap == 'Normal Map':
            st.map(route_info,size=2)
        
    else:
        st.map()

Main()