from flask import Flask, render_template, request, redirect
from airbnb_search import get_accommodation_infos
from airbnb_detail import extract_detail
from airbnb_more_review import extract_more_review

app = Flask("SuperScrapper")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scrape")
def scrape():
    query_params = get_query_params(request)
    if query_params:
        accommodation_infos = get_accommodation_infos(query_params)
        extract_detail(accommodation_infos)
        return render_template("scrapepage.html", **query_params)
    else:
        return redirect("/")

@app.route("/more_reviews")
def scrape_review():
    query_params = get_query_params(request)
    if query_params:
        accommodation_infos = get_accommodation_infos(query_params)
        extract_more_review(accommodation_infos)
        return render_template("end.html", searchingBy=query_params['place'])
    else:
        return redirect("/")

def get_query_params(request):
    place = request.args.get('place')
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    adults = request.args.get('adults')
    if place and checkin and checkout and adults:
        return {'place': place, 'checkin': checkin, 'checkout': checkout, 'adults': adults}
    return None

if __name__ == "__main__":
    app.run(host="localhost")