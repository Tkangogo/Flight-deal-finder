import os
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib

load_dotenv()
class NotificationManager:
    def __init__(self):
        self.sid = os.getenv("TWILLO_ACCOUNT_SID")
        self.authentication = os.getenv("TWILLO_AUTH_TOKEN")
        self.my_email = os.getenv("MY_EMAIL")
        self.my_password = os.getenv("MY_PASSWORD")

    def send_whatsapp_message(self, message_data):
        client = Client(self.sid,self.authentication)
        message = client.messages.create(
            from_='your twillo number',
            body=f"{message_data}",
            to='your phone number'
        )
        print(message.status)

    def send_email(self, recipient_email,message):
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.my_password)
                response = connection.sendmail(from_addr=self.my_email,
                                    to_addrs=recipient_email,
                                    msg=f"Subject:FLIGHT DEAL!! \n{message}"
                                    )
            if not response:  # sendmail() returns an empty dictionary if successful. Hence, we expect false when checking for (if response)
                print("Email sent successfully")
            else:
                print("Failed to send email:", response)
        except smtplib.SMTPException as e:
            print("Error:", e)



