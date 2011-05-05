This client library is designed to support the Blocket REST API.

Access to the API can be requested via:
http://www2.blocket.se/support/?id=18

Install:
	python setup.py install

Basic usage:
	import blocket

	b = blocket.API(app_id, api_key)
	results = b.search("volvo")
	for ad in results['ads']:
		print ad['subject']	
