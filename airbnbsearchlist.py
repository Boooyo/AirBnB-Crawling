import requests
from bs4 import BeautifulSoup

URL_BASE = "https://www.airbnb.co.kr/s/"

def get_last_page():
    # 여기서는 일단 정적으로 마지막 페이지를 6으로 설정합니다.
    return 6

def build_search_url(query):
    url = f"{URL_BASE}{query['place']}/homes?checkin={query['checkin']}&checkout={query['checkout']}&adults={query['adults']}&children=0&infants=0"
    return url

def extract_room_infos_from_page(url, page_number):
    room_infos = []
    result = requests.get(f"{url}&items_offset={page_number * 20}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "_1048zci"})
    
    for result in results:
        result_url = result.find("a")["href"]
        room_price = result.find("span", {"class": "_1p7iugi"}).get_text()
        room_idx = result_url[result_url.index('s/') + 2:result_url.index('?')]
        room_info = {"room_idx": room_idx, "room_price": room_price}
        if room_info not in room_infos:
            room_infos.append(room_info)
    
    return room_infos

def get_accommodation_infos(query):
    last_page = get_last_page()
    search_url = build_search_url(query)
    all_room_infos = []

    for page_number in range(last_page):
        print("Scraping page", page_number + 1)
        room_infos = extract_room_infos_from_page(search_url, page_number)
        all_room_infos.extend(room_infos)

    return {"query": query, "room_infos": all_room_infos}
