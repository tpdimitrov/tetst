import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 42.697708  # Your latitude +/- 5
MY_LONG = 23.321867  # Your longitude
# noinspection SpellCheckingInspection
TZID = "Europe/Sofia"
my_email = "pythoncourseday32@gmail.com"
# noinspection SpellCheckingInspection
password = "xmfxrminqtohdrjq"
password_yahoo = "Abcd1234!@#$"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# noinspection SpellCheckingInspection
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": TZID
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if sunrise >= time_now or time_now >= sunset:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="pythoncourseday32@yahoo.com",
                msg=f"Subject:ISS\n\n Look up!"
            )
