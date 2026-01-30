import requests
from bs4 import BeautifulSoup

def Weather():
    try:
        city = "your_city_name"  # You can also get this dynamically if needed
        url = f"https://www.google.com/search?q=weather+in+{city}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        temp = soup.find("span", attrs={"id": "wob_tm"}).text
        unit = soup.find("div", attrs={"id": "wob_dts"}).text
        condition = soup.find("span", attrs={"id": "wob_dc"}).text
        location = soup.find("div", attrs={"id": "wob_loc"}).text

        return f"{location} - {unit}: {temp}°C, {condition}"

    except Exception as e:
        return "Unable to fetch weather data at the moment."
