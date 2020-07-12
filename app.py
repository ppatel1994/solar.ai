from flask import Flask, request, jsonify, render_template
import json
import dataParse

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forecast")
def forecast():
    return render_template("forecast.html")

@app.route('/predict')
def predict():
    loc  = json.loads(request.args.get('a'))
    predictions = dataParse.getPredictions(loc['lat'], loc['long'])
    if predictions == "ERROR":
        return jsonify({"day1": "ERROR"})
    return jsonify({"day1": predictions[0], "day2": predictions[1],
                    "day3": predictions[2]})

if __name__ == "__main__":
    app.run(debug=True)
