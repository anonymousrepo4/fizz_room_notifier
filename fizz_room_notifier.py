import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# Configuration
URL = "https://www.the-fizz.com/nl/studentenwohnheim/utrecht/#apartment"
CHECK_INTERVAL = 60  # Check every minute
EMAIL_SENDER = "johndoe.anoynmous4@gmail.com"
EMAIL_PASSWORD = "unco hglb ookm efvw"
EMAIL_RECEIVER = "johndoe.anoynmous4@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def check_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for the "no offer" section (which means rooms are NOT available)
    no_offer_section = soup.find("div", class_="room-type-information-no-offer")
    if no_offer_section:
        print("No rooms available.")
        return False  # Rooms are NOT available

    # Check if there's an explicit "available" section (adjust based on the website's structure)
    available_section = soup.find("div", class_="room-type-information-available")  # Replace with actual class if needed
    if available_section:
        print("Rooms are available!")
        return True  # Rooms are available

    # If neither "no offer" nor "available" section is found, assume no availability
    print("Unclear availability status. Assuming no rooms available.")
    return False

def send_email():
    print("Sending email notification...")
    msg = MIMEText("A room is available! Check: " + URL)
    msg["Subject"] = "Room Available at The Fizz Utrecht!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("✅ Email notification sent!")
    except Exception as e:
        print("❌ Error sending email:", e)

if __name__ == "__main__":
    while True:
        print("Running bot loop...")  # Debugging
        if check_availability():
            send_email()
        print("Sleeping for", CHECK_INTERVAL, "seconds...")
        time.sleep(CHECK_INTERVAL)
