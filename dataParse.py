import requests
import time
from datetime import datetime
from dateutil import tz
import pandas as pd
import pickle
import warnings
import json

#returns json response from url
def getWeatherData(URL):
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "ERROR"

#loads api and returns urls for daily and hourly weather data
def getURLs(lat, long):
    #load api key
    with open('config.json') as f:
        data = json.load(f)
    API_KEY = data['API_KEY']

    #7 day weather url
    BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall?'
    URL = BASE_URL + 'lat=' + lat +'&lon=' + long
    QUERY = '&exclude=current, minutely,hourly&&units=imperial&appid=' + API_KEY
    dailyURL = URL + QUERY

    #five day 3 hour url
    BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast?'
    URL = BASE_URL + 'lat=' + lat +'&lon=' + long
    QUERY = '&&units=imperial&appid=' + API_KEY
    hourlyURL = URL + QUERY
    return {'daily': dailyURL, 'hourly': hourlyURL}

########################DAILY WEATHER DATA######################################

#takes in unix time and returns date in Y-M-D format
def getDateFromUnix(t):
    return datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')

#takes in date and returns day of year
def getDayOfYear(date):
    return date.timetuple().tm_yday

#returns date, temp, wind direction in a list from json object
def parseJson(j):
    date = getDateFromUnix(j['dt'])
    temp = j['temp']['max']
    humidity = j['humidity']
    windspeed = j['wind_speed']
    winddeg = j['wind_deg']
    return [date, temp, winddeg]

#takes in json response and returns date, temperature, and wind direction data in a dataframe for prediction
def parseDailyWeatherData(data):
    toPredict = pd.DataFrame(columns = ['Date', 'Temperature', 'WindDirection'])
    #get data from first 3 days in response
    toPredict.loc[0] = parseJson(data['daily'][0])
    toPredict.loc[1] = parseJson(data['daily'][1])
    toPredict.loc[2] = parseJson(data['daily'][2])
    toPredict['Date'] = pd.to_datetime(toPredict['Date'].str.strip(), format = '%Y/%m/%d')
    toPredict['dayOfYear'] = toPredict['Date'].apply(getDayOfYear)
    toPredict.set_index('Date', inplace = True)
    return toPredict

#takes in dataframe of and returns predictions in a list
def getPredictions(X):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        model = pickle.load(open('rf_model.sav', 'rb'))
    #Watt to kiloWatt
    predictions = list(model.predict(X)/1000)
    predictions = [int(p) for p in predictions]
    return predictions

#takes in url and returns solar radiation predictions
def runDailyPredictions(url):
    dailyData = getWeatherData(url)
    if dailyData == "ERROR":
        return "ERROR"
    parsedData = parseDailyWeatherData(dailyData)
    predictions = getPredictions(parsedData)
    return predictions

########################3-Hour WEATHER DATA#####################################

#returns 5-day weather forecast data as dictionary for date, temperature, and wind direction
def prepareWeatherData(data):
    data = data['list']
    fiveDayForecastData =  pd.DataFrame(columns = ['Date', 'Temp', 'WindDeg'])
    for i in range(len(data)):
        row = [data[i]['dt_txt'],
        data[i]['main']['temp'],
        data[i]['wind']['deg']]
        fiveDayForecastData.loc[i] = row
    fiveDayForecastData = fiveDayForecastData.to_dict('list')
    return fiveDayForecastData

#takes in url and returns weather data
def getHourlyWeatherData(URL):
    hourlyData = getWeatherData(URL)
    parsedData = prepareWeatherData(hourlyData)
    return parsedData
