USE InstagrarnDB;

-- Insta_user 테이블 생성
CREATE TABLE IF NOT EXISTS Insta_user (
    idx INT(9) NOT NULL AUTO_INCREMENT,
    email VARCHAR(300),
    phone VARCHAR(300),
    full_name VARCHAR(300),
    user_id VARCHAR(300),
    password VARCHAR(300),
    PRIMARY KEY (idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insta_likes 테이블 생성
CREATE TABLE IF NOT EXISTS Insta_likes (
    idx INT(9) NOT NULL AUTO_INCREMENT,
    user_idx INT(9) NOT NULL,
    board_idx INT(9) NOT NULL,
    PRIMARY KEY (idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insta_reply 테이블 생성
CREATE TABLE IF NOT EXISTS Insta_reply (
    idx INT(9) NOT NULL AUTO_INCREMENT,
    board_idx INT(9) NOT NULL,
    user_idx INT(9) NOT NULL,
    reply_idx INT(9) NOT NULL,
    PRIMARY KEY (idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insta_alert 테이블 생성
CREATE TABLE IF NOT EXISTS Insta_alert (
    idx INT(9) NOT NULL AUTO_INCREMENT,
    from_user_idx INT(9) NOT NULL,
    to_user_idx INT(9) NOT NULL,
    alert_type INT(9) NOT NULL,
    PRIMARY KEY (idx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insta_reply_view 뷰 생성
CREATE VIEW IF NOT EXISTS Insta_reply_view AS
SELECT u.user_id, r.board_idx, r.reply_idx
FROM Insta_reply AS r
JOIN Insta_user AS u ON r.user_idx = u.idx;

-- Insta_alert_view 뷰 생성
CREATE VIEW IF NOT EXISTS Insta_alert_view AS
SELECT u.user_id, a.from_user_idx, a.to_user_idx, a.alert_type
FROM Insta_alert AS a
JOIN Insta_user AS u ON a.from_user_idx = u.idx;
