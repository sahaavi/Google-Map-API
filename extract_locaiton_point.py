import requests
# You need to install the requests module to use this code
import json
import pandas as pd
from sqlalchemy import false

df = pd.read_csv('users.csv')

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json'

loc_point = []
loc_name = []

for index, row in df.iterrows():
    address = row['location']
    if len(address) < 1: break

    payload = dict()
    payload['address'] = address
    if api_key is not False: payload['key'] = api_key

    r = requests.get(serviceurl, params=payload)
    data = r.text

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    json.dumps(js, indent=4)

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    loc_point_combine = 'POINT('+ str(lng) + ' ' + str(lat) + ')'
    loc_point.append(loc_point_combine)
    location = js['results'][0]['formatted_address']
    loc_name.append(location)

df['exact_location'] = loc_name
df['location_point'] = loc_point

df.to_csv('users_point.csv', index=False)