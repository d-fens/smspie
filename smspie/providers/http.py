# -*- coding: utf-8 -*-

import sys
import pycurl
import urllib
import logging

try:
	from cStringIO import StringIO
except ImportError:
	from cStringIO import StringIO

class http():
	def __init__(self):
		"""
		Setup class, takes in a config for our settings
		"""
		self.logger = logging.getLogger(self.__module__)

		self.buffer = StringIO()
		self.curl = pycurl.Curl()

		self.curl.setopt(pycurl.SSL_VERIFYHOST, 1)
		self.curl.setopt(pycurl.SSL_VERIFYPEER, 0) # TODO: fix

		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 9)
		self.curl.setopt(pycurl.CONNECTTIMEOUT, 30)
		self.curl.setopt(pycurl.TIMEOUT, 30)

		# FIXME: broken in certain pycurl versions, fixes vodafone referers
		#self.curl.setopt(pycurl.AUTOREFERER, 1)

		self.curl.setopt(pycurl.VERBOSE, 0)

		self.curl.setopt(pycurl.SSLVERSION, 3)

	def get(self, url, params=None):
		if params:
			url += "?" + urllib.urlencode(params)
		self.logger.info("GET " + url)
		self.curl.setopt(pycurl.URL, url)
		self.curl.setopt(pycurl.HTTPGET, 1)

		self.buffer = StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, self.buffer.write)
		try:
			self.curl.perform()
		except pycurl.error, e:
			print e
			sys.exit()
		s = self.buffer.getvalue()
		self.buffer.close()
		self.logger.debug(s)
		return s

	def post(self, url, params=None, args=None):
		if params:
			self.curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(params))
		if args:
			url += "?" + urllib.urlencode(args)
		self.logger.info("POST " + url)
		self.curl.setopt(pycurl.URL, url)
		self.curl.setopt(pycurl.POST, 1)

		self.buffer = StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, self.buffer.write)
		try:
			self.curl.perform()
		except pycurl.error, e:
			print e
			sys.exit()
		s = self.buffer.getvalue()
		self.buffer.close()
		self.logger.debug(s)
		return s

	def close(self):
		self.curl.close()
