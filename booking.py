#booking api for tequila kiwi

import requests
import json
import datetime
from datetime import timedelta
from datetime import date
from datetime import datetime
from decouple import config

# Set the API key
API_KEY = config('API_KEY')

SEARCH_ID = config('SEARCH_ID')
BOOKING_TOKEN = config('BOOKING_TOKEN')
SESSION_ID = config('SESSION_ID')
#using the search id from the search api from letsfly.py, make a booking request

if SESSION_ID == '':
    #set to empety and make a new session
    #make random session id
    SESSION_ID = datetime.now().strftime("%Y%m%d%H%M%S")
    print('Session ID: ' + SESSION_ID)
    #set the session id to the config file
    with open('.env', 'a') as f:
        f.write('SESSION_ID=' + SESSION_ID)
        f.close()
else:
    print('Session ID: ' + SESSION_ID)


headers = { "apikey": API_KEY }

# Set the API endpoint and parameters for the "Locations" API
url = "https://tequila-api.kiwi.com/v2/bookings/check_flights"
params = {
    "search_id": SEARCH_ID,  # Replace with your desired destination airport code
    "booking_token": BOOKING_TOKEN,
    "bnum": 1,
    "adults": 1,
    "children": 0,
    "infants": 0,
    "session_id": SESSION_ID,
    "currency": "EUR",
}

#check_flights api for tequila kiwi


# Send the HTTP request
response = requests.post(url, params=params, headers=headers)

# Extract the list of flights
data = response.json()
print(data)
flights = data["data"]

# Print the list of flights
print("Here are the flights available:")
for flight in flights:
    print(flight["flyFrom"] + " to " + flight["flyTo"] + " on " + flight["local_departure"].split("T")[0])  
