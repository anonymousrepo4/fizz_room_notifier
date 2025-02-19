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
    
    # Modify this based on the website's HTML structure
    availability_section = soup.find("div", class_="apartment-availability")
    if availability_section and "available" in availability_section.text.lower():
        return True
    return False

def send_email():
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
        print("Email notification sent!")
    except Exception as e:
        print("Error sending email:", e)

if __name__ == "__main__":
    while True:
        if check_availability():
            send_email()
        time.sleep(CHECK_INTERVAL)
