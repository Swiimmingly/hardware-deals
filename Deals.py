import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
from plyer import notification


URL = "https://www.pcgamer.com/hardware/"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


# get title and the link of the Deal
def deals():
    counter = 2
    latest = "nothing"
    while counter < 7:
        article = soup.find("div", class_="listingResult small result"+str(counter))
        counter += 1
        link = article.a["href"]
        headline = article.a.header.h3.text
        if article.find("a", class_="category-link").text == "Deals":
            if headline != latest:
                send_email(link, headline)
                latest = headline
                send_notification()


# send new Deal with link to the Mail
def send_email(link, headline):
    EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
    EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    msg = EmailMessage()
    msg["Subject"] = "PCgamer Hardware Update"
    msg["From"] = EMAIL_ADDRESS  # Sender Mail goes here
    msg["To"] = "Email address"  # receiver Mail goes here
    msg.set_content("New Deals available on PCgamer! \n\n" + headline + "\n\n" + link)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # login to your gmail

        smtp.send_message(msg)


# notification
def send_notification():
    notification.notify(title="New Deals!!", message="New hardware Deals have been sent to your Email", timeout=5)


# update frequency
while True:
    deals()
    time.sleep(60*60*24) # rate of update
