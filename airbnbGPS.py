import requests
from bs4 import BeautifulSoup

def convert_address_to_latlng(query):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml"
    api_key = "AIzaSyBuSzbqsUUg0qzcvTAv3L_XkxoxXFyeAQ4"
    params = {
        "address": query,
        "key": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # HTTP 요청 오류가 발생하면 예외 발생
        html = BeautifulSoup(response.text, "html.parser")
        lat = html.select_one("location > lat").get_text()
        lng = html.select_one("location > lng").get_text()
        latlng = {'lat': lat, 'lng': lng}
        return latlng
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
