import requests
import os
import datetime as dt
from datetime import timedelta
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv()

class FlightSearch:

    def __init__(self):
        self.api_key = os.getenv("FLIGHT_SEARCH_API_KEY")
        self.api_secret = os.getenv("FLIGHT_SEARCH_API_SECRET")
        self.amadeus_url = os.getenv("amadeus_url")
        self.access_token = self.get_access_token()
        self.amadeus_header = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_access_token(self):
        # URL for getting the access token
        token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        # Data to send in the request body
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        # Headers for the request
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # Send the request
        response = requests.post(token_url, data=data, headers=headers)
        # Convert response to JSON
        token_info = response.json()
        access_token = token_info.get("access_token")
        print(f"Your token is: {access_token}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return access_token

    def get_iata_code(self,city_name):
        parameters = {
            "keyword" : city_name,
            "max" : 1
        }
        cities_endpoint = "/reference-data/locations/cities"

        response = requests.get(url=f"{self.amadeus_url}{cities_endpoint}",params=parameters,headers=self.amadeus_header)
        if response.status_code == 200:
            try:
                city_data = response.json()
                iata_code = city_data["data"][0]["iataCode"]
            except IndexError:
                print(f"IndexError: No airport code found for {city_name}.")
                return "N/A"
            except KeyError:
                print(f"KeyError: No airport code found for {city_name}.")
                return "Not Found"
            else:
                return iata_code
        else:
            print("Error:", response.status_code, response.text)

    def get_airport_name(self, iata_code):
        """Fetches airport name for a given IATA code using Amadeus API"""
        airport_city_search_endpoint = "/reference-data/locations"
        params = {"keyword": iata_code, "subType": "AIRPORT"}
        response = requests.get(url = f"{self.amadeus_url}{airport_city_search_endpoint}", params=params, headers=self.amadeus_header)
        data = response.json()
        airport_name = data["data"][0]["name"]
        return airport_name

    def get_flight_offers(self, destination):
        start_date = (dt.datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")  # Tomorrow
        end_date = (dt.datetime.now().date() + timedelta(days=6 * 30)).strftime("%Y-%m-%d")  # 6 months later

        # Function to make API request
        def fetch_flights(non_stop):
            params = {
                "originLocationCode": "LON",
                "destinationLocationCode": destination,
                "departureDate": start_date,
                "returnDate": end_date,
                "adults": 1,
                "nonStop": str(non_stop).lower(),
                "currencyCode": "GBP",
                "max": 5
            }
            response = requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers",
                                    params=params, headers=self.amadeus_header)
            return response

        # First, try fetching non-stop flights
        response = fetch_flights(non_stop=True)

        # If request fails, return a default FlightData object
        if response.status_code != 200:
            print(f"Error fetching flights for {destination}: {response.text}")
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

        data = response.json()

        # If no non-stop flights, try fetching flights with stopovers
        if not data.get("data"):
            print("No direct flights found. Searching for flights with stopovers...")
            response = fetch_flights(non_stop=False)
            data = response.json()

        # If still no flights found, return default FlightData object
        if not data.get("data"):
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

        # Find the cheapest flight
        cheapest_flight = min(data["data"], key=lambda x: float(x["price"]["total"]))

        # Extract flight details
        segments = cheapest_flight["itineraries"][0]["segments"]
        stops = len(segments) - 1
        price = cheapest_flight["price"]["total"]
        origin_airport = segments[0]["departure"]["iataCode"]
        destination_airport = segments[-1]["arrival"]["iataCode"]
        out_date = segments[0]["departure"]["at"].split("T")[0]
        return_date = cheapest_flight["itineraries"][-1]["segments"][-1]["arrival"]["at"].split("T")[0]

        return FlightData(price=price, origin_airport=origin_airport, destination_airport=destination_airport,
                          out_date=out_date, return_date=return_date, stops=stops)




