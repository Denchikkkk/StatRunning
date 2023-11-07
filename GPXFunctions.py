import gpxpy
import math
import random

import pandas    as pd
import streamlit as st

from gpxpy import gpx 

class GPXObject:

    def __init__(self,file):
        self.file = file
        self.basic_route_info = pd.DataFrame(columns=[ # The dataframe where we are going to store the GPX data. 
        'time',
        'latitude',
        'longitude',
        'elevation',
        'distance'
    ])
        
    def calculateDistanceWithLastPoint(self,point,lastPoint):
        """
        This functions uses the function from GPX "distance_3d" to calculate the
        distance in kms between the two points receveid as parameter. 
        
        The points must be of gpxpy.gpx.GPXTrackPoint type.

        input:
            - point:     coordinate 1 in GPXTrackPoint format.
            - lastPoint: coordinate 2 in GPXTrackPoint format.
        """
        return point.distance_3d(lastPoint)/1000

    def readGPXFile(self):
        """
        This function receives the uploaded file by the user and converts it to a
        GPX file by storing the coordinates information into a dataframe.
        
        input:
            - file: file uploaded by user.
        output:
            - route_info: coordinates (time, latitude, longitude, elevation, distanceCDF) stored in a dataframe. 

        """ 
        gpx_file = self.file.read()
        gpx      = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                # We initialize the variable "totalDistance" where we are going to store the cumulative distance in each point.
                # Describing a Cumulative Distribution Function (CDF).  
                totalDistance = 0 
                lastPoint = segment.points[0] # To avoid to use an if for each point, we initialize the "lastPoint" as starting point.

                for point in segment.points:
                    totalDistance += round(self.calculateDistanceWithLastPoint(point,lastPoint),4)
                    infoPoint = [point.time ,point.latitude, point.longitude, point.elevation,totalDistance]
                    self.basic_route_info.loc[len(self.basic_route_info)] = infoPoint
                    lastPoint = point

        return self.basic_route_info
    
    def getRandomColorValue(self):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        return self.rgb_to_hex((r,g,b))
    
    def calculateDistanceColors(self):
        maxDistance = math.ceil(self.basic_route_info.loc[len(self.basic_route_info)-1]['distance'])

        Colors = [self.getRandomColorValue() for i in range(maxDistance)]
        
        distanceColors = []

        for i in range(len(self.basic_route_info)):
            distanceColors.append(Colors[math.ceil(self.basic_route_info.iloc[i]['distance'])-1])
        
        self.basic_route_info['colors'] = distanceColors
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
            elevationColors.append(self.normalizeToColors(minElevation,maxElevation,elevation))

        self.basic_route_info['colors'] = elevationColors
        return self.basic_route_info
    
    def normalizeToColors(self,min,max,actualValue):
        factor = (actualValue - min) / (max - min)
        red   = int(255*factor)
        green = int(255*(1-factor))
        blue  = 0
        rgb = (red,green,blue)
        return self.rgb_to_hex(rgb)
        

    
    def rgb_to_hex(self,rgb):
        # Ensure RGB values are within the valid range (0-255)
        r, g, b = [max(0, min(255, int(x))) for x in rgb]
        
        # Convert to HEX format
        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        
        return hex_color


    