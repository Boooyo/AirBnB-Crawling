## 🙌 AirBnB - Crawling Test

###  무슨 서비스 인가요 ❓
- 해당 웹 크롤러(Web scraper)는 airbnb의 숙소 정보를 스크래핑하여 데이터베이스에 저장한다. 동적 크롤링을 위해 Selenium과 BeautifulSoup4 라이브러리를 사용하고 단순 웹 애플리케이션을 구현하기 위해 Flask framework를 사용하였다. 스크랩후에 pymysql로 MySQL에 저장합니다.

## ⚙ 개발 환경 설정

```sh
pip install pymysql --DB
pip install selenium
pip install flask --framework
pip install bs4
pip install requests
```
<br>

## ❗ 제한 사항

해당 사이트의 html 즉, class name이나 구조가 변경되면 코드 수정이 필요  

<br>

## 🧾 업데이트 내역  

* 1.0.0
    * UI 변경 및 config.py 작성
* 0.1.1
    * more review 추가
    * issue 해결 (이모트 가능)
* 0.1.0
    * 완료
    * issue : host 당부의 말에 이모트를 넣을 시 오류. ( -utf8mb4-로 전환 필요 )
* 0.0.1
    * 작업 진행 중
