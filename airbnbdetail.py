import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from config import conn
from airbnbGPS import Convert_to_latlng
from airbnbSQL import check_room_idx_in_DB, insert_room_data_in_MysqlDB, insert_room_data_in_airdnd_home_picture
from airbnbSQL import insert_room_data_in_airdnd_home_notice, insert_room_data_in_airdnd_home_bed, insert_room_data_in_airdnd_home_convenient_facility
from airbnbSQL import insert_room_data_in_airdnd_home_review, insert_room_data_in_airdnd_home_attractions_distance, insert_room_data_in_airdnd_home_use_rule
from airbnbSQL import insert_room_data_in_airdnd_home_safety_rule, insert_room_data_in_airdnd_host

os.environ["NLS_LANG"] = ".AL32UTF8"

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?adults=1&location=%EA%B4%8C&check_in=2020-10-01&check_out=2020-10-03&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
take_out_start_index = 0
db = conn.cursor()

def extract_pictures(room_idx, room_pictures):
    picture_urls = []
    for picture in room_pictures:
        try:
            picture_url = picture.find("img").attrs['src']
        except:
            picture_url = "None"
        insert_room_data_in_airdnd_home_picture(room_idx, picture_url)
        picture_urls.append(picture_url)
        if len(picture_urls) == 5:
            print("picture : ", picture_urls)
            return picture_urls

def extract_home_notice(room_idx, notice_sort, content, notice_icon):
    data_list = []
    take_out_start_index = 0
    print("길이오류 : ",len(notice_sort),len(content),len(notice_icon))
    for f_list in notice_sort:
        try:
            bring_notice_icon = notice_icon[take_out_start_index].select_one('path').attrs['d']
        except:
            bring_notice_icon = notice_icon[take_out_start_index].select_one('g > path').attrs['d']
        data_in_list = [f_list.string, content[take_out_start_index].get_text().replace("자세히 알아보기",""), bring_notice_icon]
        insert_room_data_in_airdnd_home_notice(room_idx, f_list.string, content[take_out_start_index].get_text().replace("자세히 알아보기",""), bring_notice_icon)
        data_list.append(data_in_list)
        take_out_start_index += 1
    take_out_start_index = 0
    print("data_list : ", data_list)  
    return data_list

def extract_home_bed(room_idx, bed_sort, content, bed_sort_icon): #print(room_bed_sort_icon[0].select_one('svg > path').attrs['d'])
    data_list = []
    take_out_start_index = 0
    icon_str = ""
    for f_list in bed_sort:
        for icon_list in bed_sort_icon[take_out_start_index].select('span._14tkmhr'):
            icon_str += icon_list.select_one('svg > path').attrs['d'] + "/"
        data_in_list = [f_list.string, content[take_out_start_index].string, icon_str]
        insert_room_data_in_airdnd_home_bed(room_idx, f_list.string, content[take_out_start_index].string, icon_str)
        data_list.append(data_in_list)
        take_out_start_index += 1
    take_out_start_index = 0
    print("data_list : ", data_list)  
    return data_list

def extract_convenient_facility(room_idx, convenient_facilities):
    data_list = []

    for e_list in convenient_facilities:
        try:
            convenient_facilitiy = e_list.find("div",{"class","_1nlbjeu"}).find("div").get_text()
            room_convenient_facility_icon = e_list.select_one('div._yp1t7a > svg > path').attrs['d']    
        except:
            convenient_facilitiy = e_list.find("div",{"class","_1nlbjeu"}).find("div").find("span",{"class","_krjbj"}).get_text()
            room_convenient_facility_icon = e_list.select_one('div._13tgo6a4 > svg > path').attrs['d']
        insert_room_data_in_airdnd_home_convenient_facility(room_idx, convenient_facilitiy, room_convenient_facility_icon)         
        data_list.append([convenient_facilitiy, room_convenient_facility_icon])
    return data_list

def extract_review(room_idx, extracted_list, room_rating):
    data_list = []
    for e_list in extracted_list:               
        room_reviews_name_date = e_list.select_one('div._1oy2hpi').find("div",{"class", "_1lc9bb6"}, recursive=False).get_text()
        room_reviews_name = room_reviews_name_date[:room_reviews_name_date.find("년 ")-4]
        room_reviews_date = e_list.select_one('div._1oy2hpi > div._1lc9bb6 > div').string
        room_reviews_cont = e_list.select_one('div._1y6fhhr > span').get_text()

        room_cleanliness = room_rating[0]
        room_accuracy = room_rating[1]
        room_communication = room_rating[2]
        room_position = room_rating[3]
        room_checkin = room_rating[4]
        room_cost_effectiveness = room_rating[5]

        review_dic = {'room_reviews_name':room_reviews_name, 'room_reviews_date':room_reviews_date ,'room_reviews_cont':room_reviews_cont, 
                    'room_cleanliness':room_cleanliness, 'room_accuracy':room_accuracy, 'room_communication':room_communication, 'room_position':room_position,
                    'room_checkin':room_checkin, 'room_cost_effectiveness':room_cost_effectiveness}
        insert_room_data_in_airdnd_home_review(room_idx, review_dic)
        data_list.append(review_dic)
    print("reviews : ", data_list)  
    return data_list

def extract_loc_info_distance(room_idx, distance):
    data_list = []
    for e_list in distance:
        nearby_attraction, attraction_distance = e_list.find_all("div")
        attractions = [nearby_attraction.string, attraction_distance.string]
        data_list.append(attractions)
        insert_room_data_in_airdnd_home_attractions_distance(room_idx, attractions)
    print("data_list : ", data_list)  
    return data_list

def extract_use_rule(room_idx, room_use_rules):
    data_list = []
    for e_list in room_use_rules:
        use_rule = e_list.find("span", recursive=False).get_text()
        data_list.append(use_rule)
        insert_room_data_in_airdnd_home_use_rule(room_idx, use_rule)
    print("data_list : ", data_list)
