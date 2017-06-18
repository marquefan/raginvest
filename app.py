#coding=utf-8
from flask import Flask, url_for, request, render_template, jsonify 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from signal import signal, SIGPIPE, SIG_DFL
from coinmarketcapAPI import *

app = Flask(__name__)
data = []
@app.before_first_request
def initialize():
	load_data()
	apsched = BackgroundScheduler()
	apsched.start()

	apsched.add_job(
		func=load_data,
		trigger=IntervalTrigger(seconds=5),
		id="load_data_interval",
		name="loading data from coinmarketcap",
		replace_existing=True)
def load_data():
	global data
	data = fetch_coin_data("bitcoin")
@app.route("/")
def index():
	#data = fetch_coin_data("bitcoin")
	return render_template("single_currency.html", data=data[0], currency="Bitcoin")

@app.route("/<coinname>")
def coin_data(coinname):
	data = fetch_coin_data(coinname)
	#return jsonify(data)
	return render_template("single_currency.html", data=data[0], currency=coinname)
if __name__ == "__main__":
	app.run(debug=True, threaded=True)