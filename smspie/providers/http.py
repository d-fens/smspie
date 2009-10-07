#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl
import urllib

try:
	from cStringIO import StringIO
except ImportError:
	from cStringIO import StringIO

class http():
	def __init__(self):
		"""
		Setup class, takes in a config for our settings
		"""
		self.buffer = StringIO()
		self.curl = pycurl.Curl()

		self.curl.setopt(pycurl.SSL_VERIFYHOST, 1)
		self.curl.setopt(pycurl.SSL_VERIFYPEER, 0) # TODO: fix

		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 9)
		self.curl.setopt(pycurl.CONNECTTIMEOUT, 30)
		self.curl.setopt(pycurl.TIMEOUT, 300)

		self.curl.setopt(pycurl.AUTOREFERER, 1)

		self.curl.setopt(pycurl.VERBOSE, 0)

	def get(self, url, params=None):
		if params:
			url += "?" + urllib.urlencode(params)
		self.curl.setopt(pycurl.URL, url)
		self.curl.setopt(pycurl.HTTPGET, 1)

		self.buffer = StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, self.buffer.write)
		self.curl.perform()
		s = self.buffer.getvalue()
		self.buffer.close()
		return s

	def post(self, url, params=None, args=None):
		if params:
			self.curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(params))
		if args:
			url += "?" + urllib.urlencode(args)
		self.curl.setopt(pycurl.URL, url)
		self.curl.setopt(pycurl.POST, 1)

		self.buffer = StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, self.buffer.write)
		self.curl.perform()
		s = self.buffer.getvalue()
		self.buffer.close()
		return s

	def close(self):
		self.curl.close()