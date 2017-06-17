#coding=utf-8
from flask import Flask, url_for, session, request, render_template, jsonify
from coinmarketcapAPI import *

app = Flask(__name__)

@app.route("/")
def index():
	data = fetch_coin_data("bitcoin")
	return render_template("index.html", data=data[0])

@app.route("/<coinname>")
def coin_data(coinname):
	data = fetch_coin_data(coinname)
	return jsonify(data)

if __name__ == "__main__":
	app.run(debug=True)