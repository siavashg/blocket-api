#!/usr/bin/env python
"""
Copyright (C) 2011 by Siavash Ghorbani <siavash@tricycle.se>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
This client library is designed to support the Blocket REST API.
Access to the API can be requested via:
http://www2.blocket.se/support/?id=18
"""

import json
import urllib2
from hashlib import sha1
from urllib import urlencode

class API:
	app_id = None
	api_key = None
	challenge = None
	request_hash = None

	url_base = "http://www.blocket.se/api/"
	url_search = url_base + "list.json"

	def __init__(self, app_id, api_key):
		self.app_id = app_id
		self.api_key = api_key

	def parse_response(self, response):
                data = json.loads(response)
		return data

	def generate_hash(self):
		if (self.challenge and self.api_key):
			return sha1(self.challenge + self.api_key).hexdigest()
		return None

	def perform_request (self, url, params = None, attempt = 0):
		if (attempt >= 5):
			print "Too many attempts, is your app id and api key correct?"
			return None
	
		# Base request parameters
		if (params):
			req_params = params
		else:
			req_params = {}

		req_params['app_id'] = self.app_id
		if (self.generate_hash()):
			req_params['hash'] = self.generate_hash()

		request = urllib2.Request(url + "?" + urlencode(req_params))
		response = urllib2.urlopen(request)

		# Blocket use ISO-8859-1 encoding
		http_data = response.read().decode('latin-1').encode('utf-8')

		# Get response as dict
		data = self.parse_response(http_data)

		# Handle invalid challenges
		if ("authorize" in data):
			if (data['authorize']['status'] == "NOT A VALID API-KEY"):
				# Invalid hash probably, generate new hash
				self.challenge = data['authorize']['challenge']
				attempt+=1
				return self.perform_request(url, params, attempt)

		return data

        def search (self, query, category=None, region=None):
                p = {}
                p['q'] = query

                # Category Group
                if (category):
	                p['cg'] = category

                # Caller
                if (region):
                        p['ca'] = region

                return self.perform_request(self.url_search, p)
