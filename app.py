from flask import Flask, render_template, request
import configparser
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import time

# def datetime_from_utc_to_local(utc_datetime):
#     now_timestamp = time.time()
#     offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
#     return utc_datetime + offset


app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db = SQLAlchemy()
db.init_app(app)

db.create_all()



@app.route('/')
def weather_dashboard():
    title = "home"
    return render_template('home.html', title=title)


@app.route('/results', methods=['POST'])
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

    data = get_weather_results(zip_code, api_key)
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


    return render_template('results.html',
                            location=location, temp=temp,
                           feels_like=feels_like, weather=weather, iconurl=iconurl, humidity=humidity, minimum=minimum,
                           maximum=maximum, sunrise=sunrise, dt_obj=dt_obj, letter=letter, now=now)






