from flask import Blueprint, render_template, request, redirect
import requests
from app.models import db, Result
from datetime import datetime


ui_bp = Blueprint(
    'ui_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


# App Home Page
@ui_bp.route('/')
def home():
    return render_template('home.html')


@ui_bp.route('/api/results')
def results_all():
    return {'data': [result.to_dict() for result in Result.query]}


@ui_bp.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = "91f60a2bd6de2a64e1a59d157c3e8e0b"
    if temp_units == "F":
        data = get_weather_results_imperial(zip_code, api_key)
        temp = (data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        minimum = data["main"]["temp_min"]
        maximum = data["main"]["temp_max"]
        letter = 'F'
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = (data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        minimum = data["main"]["temp_min"]
        maximum = data["main"]["temp_max"]
        letter = 'C'
    icon = data["weather"][0]["icon"]
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    weather = data["weather"][0]["main"]
    location = data["name"]
    humidity = data["main"]["humidity"]
    print(humidity)
    sunrise = data["sys"]["sunrise"]
    dt_obj = datetime.fromtimestamp(int(sunrise))
    now = datetime.now().replace(microsecond=0)
    # generate utc time now
    now_utc = datetime.utcnow()
    # convert to timestamp
    print(now_utc)
    timestamp_utc = datetime.timestamp(now_utc)
    # read timezone from data convert to integer
    tz_offset = int(data["timezone"])
    # add timezone offset
    local_timestamp = timestamp_utc + tz_offset
    print(local_timestamp)
    local_dt_obj = datetime.fromtimestamp(local_timestamp)
    print(local_dt_obj)
    # convert back to datetime object
    result = Result(location=location, temp=temp)
    db.session.add(result)
    db.session.commit()

    return render_template('results.html', location=location, temp=temp,
                           feels_like=feels_like, weather=weather, iconurl=iconurl, humidity=humidity, minimum=minimum,
                           maximum=maximum, sunrise=sunrise, dt_obj=dt_obj, letter=letter, now=now)


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def list_results():
    results = Result.query
    return render_template('results.html', results=results)
