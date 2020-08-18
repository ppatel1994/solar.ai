from flask import Flask, request, jsonify, render_template
import json
import dataParse

application = Flask(__name__)

@application.route("/")
def home():
    return render_template("main.html")

@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/forecast")
def forecast():
    return render_template("forecast.html")

@application.route('/predict')
def predict():
    loc  = json.loads(request.args.get('a'))
    lat = loc['lat']
    long = loc['long']
    URLs = dataParse.getURLs(lat, long)
    predictions = dataParse.runDailyPredictions(URLs['daily'])
    weatherData = dataParse.getHourlyWeatherData(URLs['hourly'])
    if predictions == "ERROR":
        return jsonify({"day1": "ERROR"})
    return jsonify({"day1": predictions[0], "day2": predictions[1],
                    "day3": predictions[2], 'lat-long': [loc['lat'], loc['long']],
                    'weatherData': weatherData})

if __name__ == "__main__":
    application.run(debug=True)
