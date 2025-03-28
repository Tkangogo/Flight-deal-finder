import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:

    def __init__(self):
        self.prices_sheet_url = os.getenv("PRICES_SHEET_URL")
        self.users_sheet_url = os.getenv("USERS_SHEET_URL")
        self.token = os.getenv("SHEETY_TOKEN")
        self.sheet_header ={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.prices_sheet_data ={}
        self.users_sheet_data = {}


    def get_prices_sheet_data(self):
        response =  requests.get(url=self.prices_sheet_url, headers=self.sheet_header)
        data = response.json()
        self.prices_sheet_data = data["prices"]
        return self.prices_sheet_data

    def update_iata_codes(self,flight_row_dictionary):
        put_url = f"{self.prices_sheet_url}/{flight_row_dictionary['id']}"
        put_payload = {
            "price": {
                "iataCode" : flight_row_dictionary["iataCode"],
            }
        }
        response = requests.put(url=put_url,json=put_payload,headers=self.sheet_header)
        print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_sheet_url, headers=self.sheet_header)
        data = response.json()
        self.users_sheet_data = data["users"]
        return self.users_sheet_data



