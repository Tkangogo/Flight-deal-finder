#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from dotenv import load_dotenv

load_dotenv()

flight_search = FlightSearch()
data_manager = DataManager()
notification = NotificationManager()

# get the prices sheet data
prices_sheet_data = data_manager.get_prices_sheet_data()

# Getting the users sheet data
users_sheet = data_manager.get_customer_emails()

# Getting customer emails
user_emails = [dictionary_element["whatIsYourEmail?"] for dictionary_element in users_sheet]

for email in user_emails:
    for city in prices_sheet_data:
        flight_offers = flight_search.get_flight_offers(destination=city["iataCode"])
        if flight_offers.price != "N/A" and flight_offers.stops > 0:
            flight_offer_message = f"Low price alert! Only GBP{flight_offers.price} to fly from {flight_offers.origin_airport} airport London, to {flight_offers.destination_airport} airport {city['city']} with {flight_offers.stops} stopovers along the way, on {flight_offers.out_date} until {flight_offers.return_date}"
            notification.send_email(recipient_email=email,message=flight_offer_message)
            notification.send_whatsapp_message(message_data=flight_offer_message)
        elif flight_offers.price != "N/A" and flight_offers.stops == 0:
            flight_offer_message = f"Low price alert! Only {flight_offers.price} to fly non stop from {flight_offers.origin_airport} airport London, to {flight_offers.destination_airport} airport {city['city']}, on {flight_offers.out_date} until {flight_offers.return_date}"
            notification.send_email(recipient_email=email, message=flight_offer_message)
            notification.send_whatsapp_message(message_data=flight_offer_message)







