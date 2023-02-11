# LetsFly

This project is a simple Python script that uses the Tequila API to search for the cheapest flights to a given destination airport. The script sends an HTTP request to the Tequila API with the destination airport code and other search parameters, then parses the response to extract the relevant flight information.

#Getting Started

To use this script, you will need a Tequila API key. You can obtain an API key by creating an account on the Tequila API website (https://tequila.kiwi.com/portal/).

Once you have an API key, add it to the .env file on the folder.

You will also need to have the requests and prettytable Python packages installed. You can install these packages using pip:

`pip install requests prettytable`

#Usage

To search for the cheapest flights to a given destination airport, simply run the letsfly.py script with the desired airport code as a command-line argument:

`python letsfly.py`

This will search for the cheapest flights to destination and display the results in a table.

The parameters to be entered are:

- Date of departure
- Date of Arrival
- Airport of departure
- Destination (can be an airport, city or continent)

If the date of departure is left blank, it will take the next day.
If the date of arrival is left blank, it will take 4 days forward.
If the airport of departure is left blank, it will take as default by code.
If the destination is left blank, it will take as destination 'Europe'.
