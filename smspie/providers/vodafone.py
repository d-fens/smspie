#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import re
import urllibp
import cookielib
import pycurl
from BeautifulSoup import BeautifulSoup
import logging

from http import http

class vodafone(http):
	"""
	"""
	def __init__(self, config={}):
		"""
		Setup class, takes in a config for our settings
		"""
		http.__init__(self)
		self.config = config # TODO: throw warning on required settings 

		self.logger = logging.getLogger(self.__module__)

		if 'proxy' in self.config and 'use_proxy' in self.config and self.config['use_proxy'] and self.config['proxy'] is not None:
			self.curl.setopt(pycurl.PROXY, self.config['proxy'])
		if 'user-agent' in self.config and self.config['user-agent'] is not None:
			self.curl.setopt(pycurl.USERAGENT, self.config['user-agent'])
		if 'cookiefile' in self.config and self.config['cookiefile'] is not None:
			self.curl.setopt(pycurl.COOKIEFILE, os.path.expanduser(self.config['cookiefile']))
			self.curl.setopt(pycurl.COOKIEJAR, os.path.expanduser(self.config['cookiefile']))

	def resumable(self, expiration=3600):
		"""
		"""
		resume = False
		if 'cookiefile' in self.config and self.config['cookiefile'] is not None:
			if os.path.isfile(os.path.expanduser(self.config['cookiefile'])):
				self.logger.debug("Attempting to use cookiefile %s", self.config['cookiefile'])
				try:
					cookiejar = cookielib.MozillaCookieJar(os.path.expanduser(self.config['cookiefile']))
					cookiejar.load()

					return True
					cookies = 0
					resume = True # everything loads, but lets check more!
					for index, cookie in enumerate(cookiejar):
						cookies = cookies + 1
						if int(cookie.expires) <= time.time():
							self.logger.info("%s expired %ss ago", cookie, int(cookie.expires - time.time()))
							resume = False
						else:
							self.logger.debug("%s will expire in %ss", cookie, int(cookie.expires - time.time()))
							cookie.expires = int(time.time() + expiration)
					if cookies == 0:
						resume = False

					if not resume:
						cookiejar.clear()

					cookiejar.save()
				except IOError:
					return False
		return resume

	def connect(self):
		"""
		Connects to vodafone.ie, does a check to see if meteors up and working.
		"""
		if self.resumable():
			self.logger.info("Resuming from connect.")
			return True

		handle = self.get('https://www.vodafone.ie/')
		soup = BeautifulSoup(handle)

		if soup.html.head.title.string == "Vodafone Mobile Phone Ireland - Best Mobile Phone &amp; Irish Broadband Deals From Vodafone Ireland":
			self.logger.info("connect has correct HTML title.")
			return True
		return False

	def login(self, username, password):
		"""
		Login to vodafone.ie

		Returns true if successful or false if fails.
		"""
		if self.resumable():
			self.logger.info("Resuming from login.")
			return True
		else:
			self.logger.info("Unable to resume, running connect from login.")
			self.connect()

		post = [
			('username', username),
			('password', password)
		]
		handle = self.post('https://www.vodafone.ie/myv/services/login/Login.shtml', post)
		soup = BeautifulSoup(handle)

		if soup.html.head.title.string == "My Vodafone, Webtext, Email, Upgrades, Vodafone Email Plus, Mobile Phone Offers at Vodafone.ie":
			self.logger.info("login has correct HTML title.")
			return True
		return False

	def message(self, phonenumber, message):
		"""
		Sends a message to the recipient.
		"""
		handle = self.get('https://www.vodafone.ie/myv/messaging/webtext/Setup.shtml')
		soup = BeautifulSoup(handle)
		if soup.html.head.title.string == "Web text - Vodafone Ireland":
			self.logger.info("message has correct HTML title.")

		secret = soup.find("input", {"type": "hidden", "name": "org.apache.struts.taglib.html.TOKEN"})
		if secret and secret.has_key('value'):
			secret = secret.get('value')
			self.logger.info("secret value [%s]", secret)
		else:
			self.logger.warning("no secret value, panic.")
			return False

		post = [
			('org.apache.struts.taglib.html.TOKEN', secret),
			('message', message),
			('recipients[0]', phonenumber),
			('recipients[1]', ''),
			('recipients[2]', ''),
			('recipients[3]', ''),
			('recipients[4]', ''),
			('contact_filter', 'Search contacts'),
			('futuredate', 'false'),
			('futuretime', 'false')
		]
		ref_params = [
			('ts', int(time.time())),
			('keeprecipients', 'true')
		]
		# FIXME: remove if > pycurl becomes more available
		self.curl.setopt(pycurl.REFERER, 'https://www.vodafone.ie/myv/messaging/webtext/Setup.shtml' + urllib.urlencode(ref_params))
		handle = self.post('https://www.vodafone.ie/myv/messaging/webtext/Process.shtml', post)
		soup = BeautifulSoup(handle)

		# TODO: add checking
		return True

	def import_contacts(self):
		"""
		Returns the list of contacts within the phonebook.

		If it fails, there is no checks so it returns an empty list.
		"""
		# TODO: vodafone uses webmail (at least for a nice list of all users)
		return []

