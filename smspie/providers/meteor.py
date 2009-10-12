#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import re
import cookielib
import pycurl
from BeautifulSoup import BeautifulSoup
import logging

from http import http

class meteor(http):
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
		Connects to mymeteor.ie, does a check to see if meteors up and working.
		"""
		if self.resumable():
			self.logger.info("Resuming from connect.")
			return True

		handle = self.get('https://www.mymeteor.ie/')
		soup = BeautifulSoup(handle)

		if soup.html.head.title.string == "Meteor: MyMeteor Login":
			self.logger.info("connect has correct HTML title.")
			return True
		return False

	def login(self, username, password):
		"""
		Login to mymeteor.ie

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
			('userpass', password),
			('returnTo', '/')
		]
		handle = self.post('https://www.mymeteor.ie/go/mymeteor-login-manager', post)
		soup = BeautifulSoup(handle)

		# TODO: Might be billpay, atlas says the title is different
		if soup.html.head.title.string == "Meteor: Prepay Functions":
			self.logger.info("login has correct HTML title.")
			return True
		return False

	def message(self, phonenumber, message):
		"""
		Sends a message to the recipient.
		"""
		params = [
			('event', "smsAjax"),
			('func', "addEnteredMsisdns")
		[
		post = [
			('ajaxRequest', "addEnteredMSISDNs"),
			('remove', "-"),
			('add', "0|" + phonenumber)
		]
		handle = self.post('https://www.mymeteor.ie/mymeteorapi/index.cfm', post, params)
		
		params = [
			('event', "smsAjax"),
			('func', "sendSMS")
		]
		post = [
			('ajaxRequest', "sendSMS"),
			('messageText', message)
		]
		handle = self.post('https://www.mymeteor.ie/mymeteorapi/index.cfm', post, params)

		messageSentPattern = re.compile('showEl\(\"sentTrue\"\)', re.IGNORECASE)
		for result in messageSentPattern.findall(handle):
			return True
		return False

	def import_contacts(self):
		"""
		Returns the list of contacts within the phonebook.

		If it fails, there is no checks so it returns an empty list.
		"""
		params = [
			('event', "smsAjax"),
			('func', "initFwtPhonebook"),
			('ajaxRequest', "initFwtPhonebook")
		]
		handle = self.get('https://www.mymeteor.ie/mymeteorapi/index.cfm', params)

		params = [
			('event', "smsAjax"),
			('func', "searchFWTPhonebook"),
			('ajaxRequest', "searchFwtPhonebook"),
			('searchValue', "All:single")
		]
		handle = self.get('https://www.mymeteor.ie/mymeteorapi/index.cfm', params)

		phonePattern = re.compile('\"Add\"\,\"(.+)"\,\"(08\d{8})\"\,\"(.+)\"\,\"(.+)\"', re.IGNORECASE)
		phonebook = []
		for result in phonePattern.findall(handle):
			phonebook.append({'phonenumber': result[1], 'username': result[0]})
		return phonebook

