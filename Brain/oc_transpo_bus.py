import json
import re
import pandas as pd
import requests
from load_key_from_config import getConfigKey

baseAPIOCTranspo = "https://api.octranspo1.com/v2.0"

bus_keyword = ["bus", "bus timing", "bus from", "next bus"]

def processBusRequest(text):

    # Use regular expressions with named groups to extract the locations
    pattern = r'from (?P<from_location>[\w\s]+) to (?P<to_location>[\w\s]+)'
    match = re.search(pattern, text)

    if match:
        from_station = match.group('from_location')
        to_station = match.group('to_location')
        return(getBusSchedule(from_station, to_station))
    
    elif 'route' in text:
        pattern = r'route (\d+)'
        match = re.search(pattern, text)
        if match:
            df = pd.read_csv('Database/oc_transpo_stops.csv').set_index('Stations')
            for index, row in df.iterrows():
                if index in text:
                    stopNo = row['StopNo']
            route_number = match.group(1)

            return getBusTimes(stopNo, route_number)
        
    

    

def getBusSchedule(source, destination):
    df = pd.read_csv('Database/oc_transpo_stops.csv').set_index('Stations')
    stopNo = df.loc[source, 'StopNo']

    apiKey = getConfigKey("ocTranspoAPI")
    appId = getConfigKey("ocTranspoAppId")

    ocTranspoAPI = f"{baseAPIOCTranspo}/GetRouteSummaryForStop?appID={appId}&apiKey={apiKey}&stopNo={stopNo}&format=JSON"

    response = requests.request("GET", ocTranspoAPI)

    data = json.loads(response.text)

    baseResult = ""

    for route in data['GetRouteSummaryForStopResult']['Routes']['Route']:
        if(destination in route['RouteHeading']):
            baseResult+= getBusTimes(stopNo, route['RouteNo'])
    
    return baseResult

def getBusTimes(stopNo, routeNo):

    apiKey = getConfigKey("ocTranspoAPI")
    appId = getConfigKey("ocTranspoAppId")

    ocTranspoAPI = f"{baseAPIOCTranspo}/GetNextTripsForStop?appID={appId}&apiKey={apiKey}&stopNo={stopNo}&routeNo={routeNo}&format=JSON"
    response = requests.request("GET", ocTranspoAPI)

    data = json.loads(response.text)
    routeDetails = data['GetNextTripsForStopResult']['Route']['RouteDirection']
    response = f"RouteNo: {routeDetails['RouteNo']}\nRoute Label: {routeDetails['RouteLabel']}\n"
    for trip in routeDetails['Trips']['Trip']:
        response+= f"Destination: {trip['TripDestination']}, StartTime: {trip['TripStartTime']}\n"
    return response
        
    



# print(processBusRequest('what time does the route 97 bus leave Hurdman Station?'))



