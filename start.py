from amadeus import Client, ResponseError

amadeus = Client(
    client_id='LsBh8ZowGbjGF03Cib5I3xQiimh32UR4',
    client_secret='AD2L0RoKOnIFyqKb'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='TLV',
        destinationLocationCode='LON',
        departureDate='2022-12-29',
        adults=2)
    print(response.data)
except ResponseError as error:
    print(error)