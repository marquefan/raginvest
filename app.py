#coding=utf-8
from flask import Flask, url_for, request, render_template, jsonify 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from signal import signal, SIGPIPE, SIG_DFL
from coinmarketcapAPI import *

app = Flask(__name__)

""" 

switch zu cryptowat.ch ? coinmarketcap reloaded zu selten :'(

"""

global_data = []
coinlist = {}

@app.before_first_request
def initialize():
	load_data()
	global coinlist
	for idx, coin in enumerate(global_data):
		coinlist[coin["name"].lower()] = idx
	apsched = BackgroundScheduler()
	apsched.start()

	apsched.add_job(
		func=load_data,
		trigger=IntervalTrigger(seconds=30),
		id="load_data_interval",
		name="loading data from coinmarketcap",
		replace_existing=True)

def load_data():
	global global_data
	global_data = fetch_coin_data("bitcoin")
	print "reloaded data"
@app.route("/")
def index():
	return render_template("single_currency.html", data=global_data[0], currency="Bitcoin")

@app.route("/<coinname>")
def coin_data(coinname):
	load_data()
	#data = fetch_coin_data(coinname)
	#return jsonify(data)
	return render_template("single_currency.html", data=global_data[coinlist[coinname]], currency=coinname)

# /bitcoin makes a request to this and gets a json object as response with all the data
@app.route("/getCoinData/<coinname>")
def return_coin_data(coinname):
	load_data()
	index = coinlist[coinname]
	return jsonify(global_data[index])

if __name__ == "__main__":
	app.run(debug=True, threaded=True)