USE AirdndDB;

-- 외래 키 검사 비활성화
SET FOREIGN_KEY_CHECKS = 0;

-- 테이블 데이터 삭제
TRUNCATE TABLE airdnd_home;
TRUNCATE TABLE airdnd_home_attractions_distance;
TRUNCATE TABLE airdnd_home_bed;
TRUNCATE TABLE airdnd_home_convenient_facility;
TRUNCATE TABLE airdnd_home_notice;
TRUNCATE TABLE airdnd_home_picture;
TRUNCATE TABLE airdnd_home_review;
TRUNCATE TABLE airdnd_home_safety_rule;
TRUNCATE TABLE airdnd_home_use_rule;
TRUNCATE TABLE airdnd_host;

-- 해당 홈 데이터 삭제
DELETE FROM airdnd_home WHERE home_idx = 10193201;
DELETE FROM airdnd_home_attractions_distance WHERE home_idx = 10193201;
DELETE FROM airdnd_home_bed WHERE home_idx = 10193201;
DELETE FROM airdnd_home_convenient_facility WHERE home_idx = 10193201;
DELETE FROM airdnd_home_notice WHERE home_idx = 10193201;
DELETE FROM airdnd_home_picture WHERE home_idx = 10193201;
DELETE FROM airdnd_home_review WHERE home_idx = 10193201;
DELETE FROM airdnd_home_safety_rule WHERE home_idx = 10193201;
DELETE FROM airdnd_home_use_rule WHERE home_idx = 10193201;
DELETE FROM airdnd_host WHERE home_idx = 10193201;

-- 새로운 테이블 생성
CREATE TABLE IF NOT EXISTS airdnd_home2 LIKE airdnd_home;
CREATE TABLE IF NOT EXISTS airdnd_home_attractions_distance2 LIKE airdnd_home_attractions_distance;
CREATE TABLE IF NOT EXISTS airdnd_home_bed2 LIKE airdnd_home_bed;
CREATE TABLE IF NOT EXISTS airdnd_home_convenient_facility2 LIKE airdnd_home_convenient_facility;
CREATE TABLE IF NOT EXISTS airdnd_home_notice2 LIKE airdnd_home_notice;
CREATE TABLE IF NOT EXISTS airdnd_home_picture2 LIKE airdnd_home_picture;
CREATE TABLE IF NOT EXISTS airdnd_home_review2 LIKE airdnd_home_review;
CREATE TABLE IF NOT EXISTS airdnd_home_safety_rule2 LIKE airdnd_home_safety_rule;
CREATE TABLE IF NOT EXISTS airdnd_home_use_rule2 LIKE airdnd_home_use_rule;
CREATE TABLE IF NOT EXISTS airdnd_host2 LIKE airdnd_host;

-- 외래 키 검사 활성화
SET FOREIGN_KEY_CHECKS = 1;

COMMIT;
