import pandas as pd 
import requests 
import numpy as np
import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

#Importing data and creating dataframe
url= 'https://api.spacexdata.com/v4/launches/past'
response= requests.get(url)
data=pd.json_normalize(response.json())
data_raw= data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
data_raw= data_raw[data_raw['cores'].map(len)==1]
data_raw= data_raw[data_raw['payloads'].map(len)==1]
data_raw['cores']= data_raw['cores'].map(lambda x: x[0])
data_raw['payloads']= data_raw['payloads'].map(lambda x: x[0])
data_raw['date']= pd.to_datetime(data_raw['date_utc']).dt.date

#The used functions
#first Function for Booster name
def getBoosterVersion(data_raw):
    for x in data_raw['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

#Second Function for get the launch site:
def getLaunchSite(data_raw):
    for x in data_raw['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

#Third function for the mass of the payload
def getPayloadData(data_raw):
    for load in data_raw['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])
#Fourth function  for the outcome of the landing
def getCoreData(data_raw):
    for core in data_raw['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])

#creating all parameters
BoosterVersion=[]
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

getBoosterVersion(data_raw)
getLaunchSite(data_raw)
getPayloadData(data_raw)
getCoreData(data_raw)

launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}
data= pd.DataFrame(launch_dict)
print(data.head())
