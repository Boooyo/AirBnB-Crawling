import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from config import conn

# 한글 깨짐 방지 
os.environ["NLS_LANG"] = ".AL32UTF8"

URL_BASE = "https://www.airbnb.co.kr/rooms/"
db = conn.cursor()

def insert_review_data(room_idx, review_dic):
    sql_insert = 'INSERT INTO airdnd_home_review (idx, home_idx, user_name, review_date, review_content, room_cleanliness, room_accuracy, room_communication, room_position, room_checkin, room_cost_effectiveness) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (room_idx, review_dic['room_reviews_name'], review_dic['room_reviews_date'], review_dic['room_reviews_cont'], review_dic['room_cleanliness'], review_dic['room_communication'], review_dic['room_position'], review_dic['room_accuracy'], review_dic['room_checkin'], review_dic['room_cost_effectiveness'])
    db.execute(sql_insert, val)
    conn.commit()
    print("DB 저장 성공 - airdnd_review")

def extract_review_details(review_elements, room_rating):
    reviews = []
    for element in review_elements:
        name_date = element.select_one('div._1oy2hpi').find("div", {"class", "_1lc9bb6"}, recursive=False).get_text()
        name = name_date[:name_date.find("년 ")-4]
        date = name_date[name_date.find("년 ")-4:]
        content = element.select_one('div._1y6fhhr > span').get_text()
        review = {
            'room_reviews_name': name,
            'room_reviews_date': date,
            'room_reviews_cont': content,
            'room_cleanliness': room_rating[0],
            'room_accuracy': room_rating[1],
            'room_communication': room_rating[2],
            'room_position': room_rating[3],
            'room_checkin': room_rating[4],
            'room_cost_effectiveness': room_rating[5]
        }
        insert_review_data(room_idx, review)
        reviews.append(review)
    print("reviews : ", reviews)
    return reviews

def extract_ratings(rating_elements):
    ratings = []
    for element in rating_elements:
        rating = float(element.string) if element.string else 0
        ratings.append(rating)
    if len(ratings) == 0:
        ratings = [0, 0, 0, 0, 0, 0]
    print("ratings : ", ratings)
    return ratings

def scrape_reviews(url, room_idx, place):
    driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(5)
    driver.implicitly_wait(15)
    scr1 = driver.find_element_by_xpath('/html/body/div[11]/section/div/div/div[3]/div/div/section/div/div[2]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
    time.sleep(3)
    html = driver.page_source
    time.sleep(3)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select_one('body.with-new-header')
    main_container = results.select_one('div._yzu7qn')
    load_test = main_container.select_one('div._m5uolq')

    if load_test is not None:
        review_elements = main_container.select('div._1gjypya')
        rating_elements = main_container.select('div._a3qxec > div._tk5b0r > span._4oybiu')
        room_rating = extract_ratings(rating_elements)
        reviews = extract_review_details(review_elements, room_rating)
        data = {'room_idx': room_idx, 'room_reviews': reviews}
        driver.quit()
        return data
    else:
        print("try again..")
        driver.quit()

def extract_more_review(accommodation_infos):
    query = accommodation_infos['Query']
    place = query['place']
    checkin = query['checkin']
    checkout = query['checkout']
    adults = query['adults']

    for room_info in accommodation_infos['room_infos']:
        room_idx = room_info["room_idx"]
        url = f"{URL_BASE}{room_idx}/reviews?adults={adults}&location={place}&check_in={checkin}&check_out={checkout}&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
        scrape_reviews(url, room_idx, place)

    db.close()
    conn.close()

