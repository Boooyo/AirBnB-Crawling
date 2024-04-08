import os
from config import conn

# 한글 깨짐 방지
os.environ["NLS_LANG"] = ".AL32UTF8"

URL_BASE = "https://www.airbnb.co.kr/rooms/"
take_out_start_index = 0
db = conn.cursor()

def check_room_idx_in_DB(): 
    sql_select = 'select home_idx from airdnd_home'
    db.execute(sql_select)
    room_nums_in_DB = db.fetchall()
    return room_nums_in_DB

def execute_sql(sql, values):
    try:
        db.execute(sql, values)
        conn.commit()
        print("DB 저장 성공")
    except Exception as e:
        print(f"DB 저장 실패: {e}")

def insert_room_data_in_MysqlDB(data):
    sql = 'insert into airdnd_home (home_idx, place, title, isSuperHost, addr, lat, lng, sub_title, filter_max_person, filter_bedroom, filter_bed, filter_bathroom, price, host_notice, loc_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (data['room_idx'], data['place'], data['main_title'], data['isSuperHost'], data['addr'], data['latlng']['lat'], data['latlng']['lng'], data['sub_title'], data['room_filter_max_person'], data['room_filter_bedroom'], data['room_filter_bed'], data['room_filter_bathroom'], data['price'], data['room_host'], data['room_loc_info_cont'])
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_picture(room_idx, room_picture):
    sql = 'insert into airdnd_home_picture (idx, home_idx, url) VALUES (0, %s, %s)'
    values = (room_idx, room_picture)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_notice(room_idx, room_notice_sort, room_notice_content, room_notice_icon):
    sql = 'insert into airdnd_home_notice (idx, home_idx, home_notice_sort, home_notice_content, home_notice_icon) VALUES (0, %s, %s, %s, %s)'
    values = (room_idx, room_notice_sort, room_notice_content, room_notice_icon)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_bed(room_idx, bed_room_name, bed_room_option, icon_str):
    sql = 'insert into airdnd_home_bed (idx, home_idx, bed_room_name, bed_room_option, bed_icons) VALUES (0, %s, %s, %s, %s)'
    values = (room_idx, bed_room_name, bed_room_option, icon_str)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_convenient_facility(room_idx, convenient_facilitiy, room_convenient_facility_icon):
    sql = 'insert into airdnd_home_convenient_facility (idx, home_idx, facility, facility_icon) VALUES (0, %s, %s, %s)'
    values = (room_idx, convenient_facilitiy, room_convenient_facility_icon)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_review(room_idx, review_dic):
    sql = 'insert into airdnd_home_review (idx, home_idx, user_name, review_date, review_content, room_cleanliness, room_accuracy, room_communication, room_position, room_checkin, room_cost_effectiveness) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (room_idx, review_dic['room_reviews_name'], review_dic['room_reviews_date'], review_dic['room_reviews_cont'], review_dic['room_cleanliness'], review_dic['room_communication'], review_dic['room_position'], review_dic['room_accuracy'], review_dic['room_checkin'], review_dic['room_cost_effectiveness'])
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_attractions_distance(room_idx, attractions):
    sql = 'insert into airdnd_home_attractions_distance (idx, home_idx, attractions_name, attractions_distance) VALUES (0, %s, %s, %s)'
    values = (room_idx, attractions[0], attractions[1])
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_use_rule(room_idx, use_rule):
    sql = 'insert into airdnd_home_use_rule (idx, home_idx, use_rule) VALUES (0, %s, %s)'
    values = (room_idx, use_rule)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_home_safety_rule(room_idx, safety):
    sql = 'insert into airdnd_home_safety_rule (idx, home_idx, safety_rule) VALUES (0, %s, %s)'
    values = (room_idx, safety)
    execute_sql(sql, values)

def insert_room_data_in_airdnd_host(room_idx, host_data):
    sql = 'insert into airdnd_host (idx, home_idx, host_name, host_sign_in_date, check_superhost, check_certification, host_review_num, host_status_message, Interaction_with_guests, host_language, response_rate, response_time) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (room_idx, host_data['room_host_name'], host_data['room_host_sign_in_date'], host_data['room_host_superhost'], host_data['room_host_certification'], host_data['room_host_review_num'], host_data['room_host_stats'], host_data['room_host_interaction'], host_data['host_language'], host_data['host_response_rate'], host_data['host_response_time'])
    execute_sql(sql, values)
