import gpxpy

import pandas    as pd
import streamlit as st

from gpxpy import gpx

# We configure Streamlit WebApp. 
st.set_page_config(page_title='Map Tracker', page_icon='📊')
st.title('Fake Strava')

# The dataframe where we are going to store the GPX data. 
route_info = pd.DataFrame(columns=[
    'latitude',
    'longitude',
    'elevation'
])

def calculateElevationColors():
    """
    This function calculates the color of the point on the map, depending on the elevation.
    In this case, when the point is closer to max elevation of the track, it is colored with red.
    While if it is closer to min elevation the point is more greener.
    
    - output:
        route_info: the dataframe with a new color column for each point in '#FFFFFF' format.  
    """
    maxElevation = route_info['elevation'].max()
    minElevation = route_info['elevation'].min()

    elevationColors = []

    for i in range(len(route_info)):
        elevation = route_info.iloc[i]['elevation']
        factor = (elevation - minElevation) / (maxElevation - minElevation)

        red   = int(255*factor)
        green = int(255*(1-factor))
        blue  = 0
        color = rgb_to_hex((red,green,blue))
        elevationColors.append(color)

    route_info['colors'] = elevationColors
    return route_info

def readGPXFile(file):
    """
    This function receives the uploaded file by the user and converts it to a
    GPX file by storing the coordinates into a dataframe.
    
    input:
        - file: file uploaded by user.
    output:
        - route_info: coordinates (latitude, longitude, elevation) stored in a dataframe. 

    """ 
    gpx_file = file.read()
    gpx      = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                infoPoint = [point.latitude, point.longitude, point.elevation]
                route_info.loc[len(route_info)] = infoPoint
    return route_info

def rgb_to_hex(rgb):
    # Ensure RGB values are within the valid range (0-255)
    r, g, b = [max(0, min(255, int(x))) for x in rgb]
    
    # Convert to HEX format
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    
    return hex_color


def Main():
    
    file = st.file_uploader('Choose the GPX file.', type=['gpx'])
    if file:
        typeOfMap = st.radio('How do you want to visualize your map?',['Normal Map','Elevation Map'])
        readGPXFile(file)
        if typeOfMap == 'Elevation Map':
            route_infoColors = calculateElevationColors()
            st.map(route_infoColors,color='colors',size=2)
            st.line_chart(route_info['elevation'])
        elif typeOfMap == 'Normal Map':
            st.map(route_info,size=2)
    else:
        st.map()

Main()