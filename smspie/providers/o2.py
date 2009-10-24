# -*- coding: utf-8 -*-
import os
import time
import re
import cookielib
import pycurl
from BeautifulSoup import BeautifulSoup
import logging

from http import http

class o2(http):
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
		Connects to o2online.ie, does a check to see if o2s up and working.
		"""
		if self.resumable():
			self.logger.info("Resuming from connect.")
			return True

		handle = self.get('http://www.o2online.ie/wps/wcm/connect/O2/Home/')
		soup = BeautifulSoup(handle)

		if unicode(soup.html.head.title.string).strip() == u"Mobile Phones – Prepaid Phones – Bill Pay Phones – Mobile Broadband - Broadband Deals - with O2 Ireland":
			self.logger.info("connect has correct HTML title.")
			return True
		return False

	def login(self, username, password):
		"""
		Login to o2online.ie

		Returns true if successful or false if fails.
		"""
		if self.resumable():
			self.logger.info("Resuming from login.")
			return True
		else:
			self.logger.info("Unable to resume, running connect from login.")
			self.connect()

		post = [
			('IDButton', 'Go'),
			('org', 'o2ext'),
			('CONNECTFORMGET', 'TRUE'),
			('IDToken1', username),
			('IDToken2', password)
		]

		handle = self.post('https://www.o2online.ie/amserver/UI/Login', post)
		from html5lib import HTMLParser, treebuilders
		parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
		soup = parser.parse(handle)

		if unicode(soup.html.head.title.string).strip() == u"LoginCheck":
			self.logger.info("login has correct HTML title.")
			return True
		return False

	def message(self, phonenumber, message):
		"""
		Sends a message to the recipient.
		"""
		params = [
			('APIID', 'AUTH-WEBSSO'),
			('TargetApp', 'o2om_smscenter_new.osp?MsgContentID=-1&SID=_'),
			('utm_source', 'dashboard_webtext_link'),
			('utm_medium', 'link'),
			('utm_campaign', 'o2_dashboard'),
		]
		self.get('http://messaging.o2online.ie/ssomanager.osp', params)

		params = [
			('MsgContentID', '-1'),
			('SID', '_'),
			('SID', '8240509_utusnutl')
		]
		handle = self.get('http://messaging.o2online.ie/o2om_smscenter_new.osp', params)

		result = re.search('Number of free text messages remaining this month: <strong>(?P<remaining>\d+)</strong>', handle, re.IGNORECASE)
		if result:
			self.remaning = result.group('remaining')

		from html5lib import HTMLParser, treebuilders
		parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
		soup = parser.parse(handle)

		form = soup.find("form", {"name": "frmSMS"})
		if not form:
			self.logger.info("no form")
			return False
		inputs = form.findAll("input", {"type": "Hidden"})
		if not inputs:
			self.logger.info("no inputs")
			return False

		post = []
		for i in inputs:
			post.append((i.get('name'), i.get('value')))
		post.append(('SMSTo', phonenumber))
		post.append(('selcountry', '00355'))
		post.append(('SMSText', message))

		params = [
			('MsgContentID', '-1'),
			('SID', '_'),
			('SID', '8240509_utusnutl')
		]
		handle = self.post('http://messaging.o2online.ie/smscenter_send.osp', post, params)

		return False

	def import_contacts(self):
		"""
		Returns the list of contacts within the phonebook.

		If it fails, there is no checks so it returns an empty list.
		"""
		return []

