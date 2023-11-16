import gpxpy
import time

import pandas    as pd
import streamlit as st

from datetime     import datetime
from gpxpy        import gpx
from GPXFunctions import GPXObject

# We configure Streamlit WebApp. 
st.set_page_config(page_title='Map Tracker', page_icon='📊')
st.title('Fake Strava')

def Main():
    file = st.file_uploader('Choose the GPX file.', type=['gpx'])

    if file:
        typeOfMap     = st.radio('How do you want to visualize your map?',['Normal Map','Elevation Map','Kilometers / Miles Map'])
        gpxInfo       = GPXObject(file)
        
        route_info    = gpxInfo.readGPXFile()

        initialTime = route_info.iloc[0]['time']
        finalTime   = route_info.iloc[-1]['time']
        totalTime   = (finalTime - initialTime)
        
        totalDistance = round(route_info.iloc[-1]['distance'],2)
        
        rythm       = time.strftime("%M:%S",time.gmtime(totalTime.seconds/totalDistance))
        rythmxKM, seconds    = gpxInfo.CalculateRythmXKm()

        totalDistancestr = str(totalDistance) 
        totalTimestr     = str(totalTime).replace('0 days ', '')
        
        st.header('Total distance: :red[' + totalDistancestr+'] km | Total Time: :green['+totalTimestr+']')
        st.header('Rythm: :blue[' + rythm +'] min/km')

        if typeOfMap == 'Elevation Map':
            route_infoColors = gpxInfo.calculateElevationColors()

            # Map plot. The points will draw the segment done. 
            st.map(route_infoColors,color='colors',size=2)

            # Line Chart Plot. X-axis = Distance (in KM.) Y-axis = Height (respective to the level of the sea.)
            chart_data = route_info[['distance','elevation']].set_index('distance')
            st.area_chart(chart_data,color='#FF0000')

        elif typeOfMap == 'Normal Map':
            st.map(route_info,size=2)

        elif typeOfMap == 'Kilometers / Miles Map':
            route_infoColors = gpxInfo.calculateDistanceColors()
            st.map(route_infoColors, color='colors',size=2)
        
        st.line_chart(rythmxKM,x='KM',y='Rythm')
        
    else:
        st.map()

Main()