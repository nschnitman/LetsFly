import requests
import argparse
from prettytable import PrettyTable
from datetime import datetime, timedelta
from decouple import config


#cmd arguments
parser = argparse.ArgumentParser()
#add option for -d to search for destination
parser.add_argument("-d", "--flyTo", help="Enter destination airport code", default='europe', nargs='?')
#add option for -f to search for departure
parser.add_argument("-f", "--flyFrom", help="Enter departure airport code", default='TLV', nargs='?')
#add option for -t to search for departure date
parser.add_argument("-t", "--dateFrom", help="Enter departure date as DD/MM/YYYY", default='', nargs='?', type=str,  metavar='today/tomorrow')
#add option for -r to search for return date
parser.add_argument("-r", "--returnFrom", help="Enter return date as DD/MM/YYYY", default='', nargs='?', type=str)
#add option for -v to show version
parser.add_argument("-v", "--version", help="Show version", default='', nargs='?', type=str)
#add option for -s to show search
parser.add_argument("-s", "--search", help="Show search", default='', nargs='?', type=str)
#add option for -p to show price
parser.add_argument("-p", "--price", help="Show price", default='', nargs='?', type=str)
#add option for -c to show cheapest
parser.add_argument("-c", "--cheapest", help="Show cheapest", default='', nargs='?', type=str)
#add option for -e to show expensive
parser.add_argument("-e", "--expensive", help="Show expensive", default='', nargs='?', type=str)
#add option for -a to show all
parser.add_argument("-a", "--all", help="Show all", default='', nargs='?', type=str)

args = parser.parse_args()

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
flyFrom = args.flyFrom
flyTo = args.flyTo
dateFrom = args.dateFrom
returnFrom = args.returnFrom

print("Welcome to the search engine. Find the best deals for your next trip! We recomend to search for flights to Europe.")

today = datetime.now()
if flyFrom == '' or flyFrom == None:
    flyFrom = 'TLV' #Change to your departure airport code
if flyTo == '' or flyTo == None:
    flyTo = 'europe' #Change to your destination airport code

#if both dates are valid dates
if dateFrom != 'today' and dateFrom != 'tomorrow' and dateFrom != '' and dateFrom != None and returnFrom != 'today' and returnFrom != 'tomorrow' and returnFrom != '' and returnFrom != None:
    departure = datetime.strptime(dateFrom, '%d/%m/%Y')
    returnDate = datetime.strptime(returnFrom, '%d/%m/%Y')

#if both dates are empty
if (dateFrom == '' or dateFrom == None) and (returnFrom == '' or returnFrom == None): 
    if today.weekday() == 0:
        departure = today + timedelta(days=3)
        returnDate = today + timedelta(days=7)
    elif today.weekday() == 1:
        departure = today + timedelta(days=2)
        returnDate = today + timedelta(days=6)
    elif today.weekday() == 2:
        departure = today + timedelta(days=8)
        returnDate = today + timedelta(days=12)
    elif today.weekday() == 3:
        departure = today + timedelta(days=7)
        returnDate = today + timedelta(days=11)
    elif today.weekday() == 4:
        departure = today + timedelta(days=6)
        returnDate = today + timedelta(days=10)
    elif today.weekday() == 5:
        departure = today + timedelta(days=5)
        returnDate = today + timedelta(days=9)
    elif today.weekday() == 6:
        departure = today + timedelta(days=4)
        returnDate = today + timedelta(days=8)
    dateFrom = departure.strftime('%d/%m/%Y')
    returnFrom = returnDate.strftime('%d/%m/%Y')
    print('You did not enter a date, so we chose the best dates for you')

#if departure date is today
if dateFrom == 'today':
    departure = today
    dateFrom = today.strftime('%d/%m/%Y')

#if departure date is tomorrow
if dateFrom == 'tomorrow': 
    departure = today + timedelta(days=1) #Return the next day
    dateFrom = departure.strftime('%d/%m/%Y')

#if dateFrom is a valid date (Not today or tomorrow or empty)
if dateFrom != 'today' and dateFrom != 'tomorrow' and dateFrom != '' and dateFrom != None and returnFrom == '' or returnFrom == None:
    departure = datetime.strptime(dateFrom, '%d/%m/%Y')
    returnDate = departure + timedelta(days=4) #Return 4 days later
    returnFrom = returnDate.strftime('%d/%m/%Y')

#If return date is empty or today or None
if (returnFrom == '' or returnFrom == 'today' or returnFrom == None):
    returnDate = today + timedelta(days=4) #Return 4 days later
    returnFrom = returnDate.strftime('%d/%m/%Y')

#if return date is tomorrow
if returnFrom == 'tomorrow':
    returnDate = today + timedelta(days=5) #Return 5 days later
    returnFrom = returnDate.strftime('%d/%m/%Y')

#if returnFrom is a valid date (Not today or tomorrow or empty)
if returnFrom != 'today' and returnFrom != 'tomorrow' and returnFrom != '' and returnFrom != None and dateFrom == '' or dateFrom == None:
    returnDate = datetime.strptime(returnFrom, '%d/%m/%Y')
    departure = returnDate - timedelta(days=4) #Leave 4 days before return
    dateFrom = departure.strftime('%d/%m/%Y')

#if departure date is before today and not today and return date is before today and not today
if departure < today and departure != today and returnDate < today and returnDate != today:
    print('Please enter a valid departure date')
    print('Today is ' + today.strftime('%d/%m/%Y'))
    print('You entered ' + departure.strftime('%d/%m/%Y') + ' as departure date')
    exit()
#if return date is before departure date
if returnDate < departure:
    print('Please enter a valid return date')
    print('Today is ' + today.strftime('%d/%m/%Y'))
    print('You entered ' + returnFrom + ' as return date')
    exit()
#If departure date is today
if departure == today:
    print('You are leaving today')
#If return date is today
if returnDate == today:
    print('Please enter a valid return date')
#If departure date is the same as return date
if returnDate == departure:
    print('Please enter a valid departure/return date')


#Print the search
print("This is the search you have entered:")
print("Departure airport: " + flyFrom)
print("Destination airport: " + flyTo)
print("Departure date: " + dateFrom)
print("Return date: " + returnFrom)
print("")



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

#if empty results
if not flights:
    print("There are no results for your search. Please try again.")
    exit()

print("Here are the results:")
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


#cmd arguments





