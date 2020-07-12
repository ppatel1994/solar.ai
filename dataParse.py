import requests
import time
from datetime import datetime
from dateutil import tz
import pandas as pd
import pickle
import warnings

#takes in unix time and returns date
def getDateFromUnix(t):
    return datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')

#returns date, temp, wind direction from json object
def parseJson(j):
    date = getDateFromUnix(j['dt'])
    temp = j['temp']['max']
    humidity = j['humidity']
    windspeed = j['wind_speed']
    winddeg = j['wind_deg']
    return [date, temp, winddeg]

#returns day of year from date
def dayOfYear(date):
    return date.timetuple().tm_yday

#returns weather data from open weather map as json object (strings as input)
def getWeatherData(lat, long):
    BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall?'
    URL = BASE_URL + 'lat=' + lat +'&lon=' + long
    QUERY = '&exclude=current, minutely,hourly&&units=imperial&appid=f6ac64f0e3e6c98ad98fe535d514e0b1'
    URL = URL + QUERY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "ERROR"

#creates dataframe for ML algorithm
def prepareData(data):
    toPredict = pd.DataFrame(columns = ['Date', 'Temperature', 'WindDirection'])
    toPredict.loc[0] = parseJson(data['daily'][0])
    toPredict.loc[1] = parseJson(data['daily'][1])
    toPredict.loc[2] = parseJson(data['daily'][2])
    toPredict['Date'] = pd.to_datetime(toPredict['Date'].str.strip(), format = '%Y/%m/%d')
    toPredict['dayOfYear'] = toPredict['Date'].apply(dayOfYear)
    toPredict.set_index('Date', inplace = True)
    return toPredict

#returns predictions
def getPredictions(lat, long):
    weatherData = getWeatherData(lat, long)
    if weatherData == "ERROR":
        return "ERROR"
    toPredict = prepareData(weatherData)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        model = pickle.load(open('rf_model.sav', 'rb'))
    predictions = list(model.predict(toPredict)/1000)
    predictions = [int(x) for x in predictions]
    return predictions
