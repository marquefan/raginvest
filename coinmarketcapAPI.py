#coding=utf-8
import urllib2, json, time
def fetch_coin_data(coin):
	time_start = time.clock()
	url = "https://api.coinmarketcap.com/v1/ticker/" + str(coin)
	ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"
	head = {"User-agent": ua}
	try:
		request = urllib2.Request(url, None, head)
		response =urllib2.urlopen(request).read()

		jsonResponse = json.loads(response)
		print "took: ", time.clock() - time_start, "ms"
		return jsonResponse
	except:
		print "ERROR, couldnt fetch data with: ",coin