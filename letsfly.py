import requests
from prettytable import PrettyTable
from datetime import datetime, timedelta
from decouple import config

# Set the API key
api_key = config('API_KEY')

# Set the API endpoint and parameters for the "Locations" API
url = "https://tequila-api.kiwi.com/locations/query"
params = {
    "term": "MAD",  # Replace with your desired destination airport code
    "location_types": "airport",
    "active_only": True
}
headers = {
    "apikey": api_key  # Replace with your own Tequila API key on the .env file
}

# Send the HTTP request
response = requests.get(url, params=params, headers=headers)

# Extract the destination airport ID
data = response.json()
destination_id = data["locations"][0]["id"]
print("Welcome to the search engine. Find the best deals for your next trip! We recomend to search for flights to Europe.")
dateFrom = input('Enter departure date as DD/MM/YYYY:  ')
returnFrom = input('Enter return date as DD/MM/YYYY: ')
flyFrom = input('Enter departure airport code: ')
flyTo = input('Enter destination airport code: ')
today = datetime.now()
if flyFrom == '':
    flyFrom = 'TLV' #Change to your departure airport code
if flyTo == '':
    flyTo = 'europe' #Change to your destination airport code
if dateFrom == '':
    departure = today + timedelta(days=1) #Return the next day
    dateFrom = departure.strftime('%d/%m/%Y')
if returnFrom == '':
    returnDate = today + timedelta(days=4) #Return 4 days later
    returnFrom = returnDate.strftime('%d/%m/%Y')

#Safety check for valid dates
try:
    datetime.strptime(dateFrom, '%d/%m/%Y')
    datetime.strptime(returnFrom, '%d/%m/%Y')
except ValueError:
    print('Please enter a valid date')
    exit()

#Safety check for dates
if dateFrom < today.strftime('%d/%m/%Y'):
    print('Please enter a valid departure date')
    exit()
if returnFrom < dateFrom:
    print('Please enter a valid return date')
    exit()

#Safety check for airport codes
if len(flyFrom) != 3 or len(flyTo) != 3:
    print('Please enter a valid airport code')
    exit()



# Set the API endpoint and parameters for the "Routes" API
url = "https://tequila-api.kiwi.com/v2/search"
params = {
    "fly_from": flyFrom,
    "fly_to": flyTo,  
    "partner_market": "us",
    "limit": 1000,
    "sort": "price",
    "asc": 1,
    "date_from": dateFrom,
    "date_to": dateFrom,
    "return_from": returnFrom,
    "return_to": returnFrom,
    "flight_type": "round",
}
# Send the HTTP request
response = requests.get(url, params=params, headers=headers)

# Extract the list of flights
data = response.json()
flights = data["data"]

# Create a set to keep track of unique airports
unique_airports = set()

# Create a PrettyTable instance
table = PrettyTable()
table.field_names = ["City", "Departure Date", "Arrival Date", "Price"]
table.align["City"] = "l"
# Add rows to the table for each unique airport
for flight in flights:
    route = flight["route"][0]
    airport = route["cityTo"]
    if airport not in unique_airports:
        departure_date = route["local_departure"].split("T")[0]
        arrival_date = flight["route"][1]["local_arrival"].split("T")[0]
        row = [
            flight["cityTo"],
            departure_date,
            arrival_date,
            flight["price"]
        ]
        table.add_row(row)
        unique_airports.add(airport)

# Print the table
print(table)
print("Thank you for using our search engine. We hope you will find the best deal for your next trip!")