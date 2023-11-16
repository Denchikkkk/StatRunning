import gpxpy
import math
import random
import time

import pandas    as pd
import streamlit as st

from Coloring import Coloring
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
    
    def calculateDistanceColors(self):
        maxDistance = self.getMaxDistanceInt()
        Colors = [Coloring.getRandomColorValue() for i in range(maxDistance)]
        
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
            elevationColors.append(Coloring.normalizeToColors(min=minElevation,max=maxElevation,actualValue=elevation))

        self.basic_route_info['colors'] = elevationColors

        return self.basic_route_info
    
    def CalculateRythmXKm(self):
        
        RythmxKMDF = pd.DataFrame(columns=[
            'KM',
            'Rythm'
        ])
        
        maxDistance = self.getMaxDistanceInt()
        for km in range(1,maxDistance):
            times = self.basic_route_info[(self.basic_route_info['distance']<=km) & (self.basic_route_info['distance']>=km-1)]
            startKMTime = times.iloc[0]['time']
            endKMTime   = times.iloc[-1]['time']
            KMTime      = endKMTime-startKMTime
            rythm       = time.strftime("%M:%S",time.gmtime(KMTime.seconds))
            minutes,seconds = divmod(KMTime.seconds,60)
            RythmxKMDF.loc[len(RythmxKMDF)] = [km,KMTime.seconds]

        return RythmxKMDF,seconds
    
    def getMaxDistanceInt(self):
        return math.ceil(self.basic_route_info.loc[len(self.basic_route_info)-1]['distance'])


    