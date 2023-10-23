import gpxpy

import pandas as pd
import streamlit as st

from gpxpy import gpx 

class GPXObject:

    def __init__(self,file):
        self.file = file
        self.basic_route_info = pd.DataFrame(columns=[ # The dataframe where we are going to store the GPX data. 
        'latitude',
        'longitude',
        'elevation'
    ])

    def readGPXFile(self):
        """
        This function receives the uploaded file by the user and converts it to a
        GPX file by storing the coordinates into a dataframe.
        
        input:
            - file: file uploaded by user.
        output:
            - route_info: coordinates (latitude, longitude, elevation) stored in a dataframe. 

        """ 
        gpx_file = self.file.read()
        gpx      = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    infoPoint = [point.latitude, point.longitude, point.elevation]
                    self.basic_route_info.loc[len(self.basic_route_info)] = infoPoint
        return self.basic_route_info

    def calculateElevationColors(self):
        """
        This function calculates the color of the point on the map, depending on the elevation.
        In this case, when the point is closer to max elevation of the track, it is colored with red.
        While if it is closer to min elevation the point is more greener.
        
        - output:
            route_info: the dataframe with a new color column for each point in '#FFFFFF' format.  
        """
        maxElevation = self.basic_route_info['elevation'].max()
        minElevation = self.basic_route_info['elevation'].min()

        elevationColors = []

        for i in range(len(self.basic_route_info)):
            elevation = self.basic_route_info.iloc[i]['elevation']
            factor = (elevation - minElevation) / (maxElevation - minElevation)

            red   = int(255*factor)
            green = int(255*(1-factor))
            blue  = 0
            rgb = (red,green,blue)
            color = self.rgb_to_hex(rgb)
            elevationColors.append(color)

        self.basic_route_info['colors'] = elevationColors
        return self.basic_route_info
    
    def rgb_to_hex(self,rgb):
        # Ensure RGB values are within the valid range (0-255)
        r, g, b = [max(0, min(255, int(x))) for x in rgb]
        
        # Convert to HEX format
        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        
        return hex_color


    