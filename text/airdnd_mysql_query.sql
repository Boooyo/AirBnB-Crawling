-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS AirdndDB CHARACTER SET=utf8;
COMMIT;
SHOW DATABASES;

-- 데이터베이스 선택
USE AirdndDB;

-- 테이블 및 뷰 삭제
DROP VIEW IF EXISTS airdnd_search_view100;
DROP VIEW IF EXISTS airdnd_facility_view;
DROP VIEW IF EXISTS airdnd_search_view2;
DROP VIEW IF EXISTS airdnd_search_view_sub;
DROP VIEW IF EXISTS airdnd_search_view_final;
DROP VIEW IF EXISTS airdnd_review_info;

-- 테이블 및 뷰 생성
CREATE TABLE IF NOT EXISTS airdnd_home (
    home_idx INT NOT NULL UNIQUE PRIMARY KEY, 
    place VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    isSuperHost BOOLEAN NOT NULL,
    addr VARCHAR(500) NOT NULL,
    lat VARCHAR(30) NOT NULL,
    lng VARCHAR(30) NOT NULL,
    sub_title VARCHAR(500) NOT NULL,
    filter_max_person INT NOT NULL,
    filter_bedroom INT NOT NULL,
    filter_bed INT NOT NULL,
    filter_bathroom INT NOT NULL,
    price INT NOT NULL,
    host_notice TEXT NOT NULL,
    loc_info VARCHAR(5000)
) ENGINE=InnoDB CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS airdnd_user (
    user_idx INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    pwd VARCHAR(100) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    first_name VARCHAR(200) NOT NULL,
    birthday DATE NOT NULL,
    profileImg VARCHAR(100),
    phone VARCHAR(100),
    signupDate DATE NOT NULL,
    description TEXT(10000)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 뷰 생성
CREATE VIEW airdnd_search_view_final AS 
SELECT v.place, v.home_idx, v.isSuperHost, v.sub_title, v.title, v.filter_max_person,
    v.filter_bedroom, v.filter_bed, v.filter_bathroom, v.price, v.rating, v.review_num, v.lat, v.lng, v.host_language,
    s.facility
FROM (
    SELECT h.place, h.home_idx, h.isSuperHost, h.sub_title, h.title, h.filter_max_person,
        h.filter_bedroom, h.filter_bed, h.filter_bathroom, h.price, 
        ROUND(((AVG(h_r.room_cleanliness) + AVG(h_r.room_accuracy) + AVG(h_r.room_communication) + 
        AVG(h_r.room_position) + AVG(h_r.room_checkin) + AVG(h_r.room_cost_effectiveness)) / 6), 1) AS rating, 
        COUNT(*) AS review_num, h.lat, h.lng, h_host.host_language 
    FROM airdnd_home AS h
    JOIN airdnd_home_review AS h_r ON h_r.home_idx = h.home_idx
    JOIN airdnd_host AS h_host ON h_host.home_idx = h.home_idx
    GROUP BY h_r.home_idx
) AS v
JOIN (
    SELECT home_idx, GROUP_CONCAT(facility) AS facility
    FROM airdnd_home_convenient_facility
    GROUP BY home_idx
) AS s ON v.home_idx = s.home_idx;

CREATE VIEW airdnd_search_view_sub AS 
SELECT home_idx, GROUP_CONCAT(facility) AS facility
FROM airdnd_home_convenient_facility
GROUP BY home_idx;

CREATE VIEW airdnd_search_view2 AS 
SELECT v.place, v.home_idx, v.isSuperHost, v.sub_title, v.title, v.filter_max_person,
    v.filter_bedroom, v.filter_bed, v.filter_bathroom, v.price, v.rating, v.review_num, v.lat, v.lng, h.host_language
FROM airdnd_search_view_final AS v
JOIN airdnd_host AS h ON v.home_idx = h.home_idx;

CREATE VIEW airdnd_search_views_ex AS 
SELECT h.home_idx, h.isSuperhost, h.sub_title, h.title, h.filter_max_person, h.filter_bedroom, h.filter_bed, h.filter_bathroom, h.price, h.lat, h.lng, hs.host_language
FROM airdnd_home AS h
JOIN airdnd_search_view_sub AS cf ON h.home_idx = cf.home_idx
JOIN airdnd_host AS hs ON h.home_idx = hs.home_idx;

CREATE VIEW airdnd_review_info AS 
SELECT home_idx, ROUND(AVG((room_cleanliness + room_accuracy + room_communication + room_position + room_checkin + room_cost_effectiveness) / 6), 1) AS rating, COUNT(*) AS review_num
FROM airdnd_home_review
GROUP BY home_idx;

CREATE VIEW airdnd_search_views_ex2 AS 
SELECT h.home_idx, h.isSuperhost, h.sub_title, h.title, h.filter_max_person, h.filter_bedroom, h.filter_bed, h.filter_bathroom, h.price, h.lat, h.lng, hs.host_language, ri.rating, ri.review_num
FROM airdnd_home AS h
JOIN airdnd_search_view_sub AS cf ON h.home_idx = cf.home_idx
JOIN airdnd_host AS hs ON h.home_idx = hs.home_idx
JOIN airdnd_review_info AS ri ON h.home_idx = ri.home_idx;
