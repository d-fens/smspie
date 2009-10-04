Python application for sending SMS via the providers web interface
========================================================================

About
------------
Send SMS messages.

Usage
------------

	Usage: smspie 08x-xxxxxxx

	Send SMS via command line

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -C PROVIDER, --provider=PROVIDER
		                sets the SMS provider
	  -c CONFIG, --config=CONFIG
		                sets path to the config file
	  -i, --import-contacts
		                import meteor contacts, copy and paste into the config
		                file
	  -l, --list            list the people in your phonebook
	  -m MESSAGE, --message=MESSAGE
		                the message you want to send
	  -u USERNAME, --username=USERNAME
		                set your username
	  -p PASSWORD, --password=PASSWORD
		                set your password

Installation
------------
To install run this as root: `python setup.py install`

To do a local install do: `python setup.py install --home="$HOME"`

Now see below on how to use it!

Examples
------------

