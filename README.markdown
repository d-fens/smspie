SMSPie
=============================================================================

About
------------
Send SMS messages using the providers website.

As of writting it supports:

* meteor.ie
* o2.ie
* vodafone.ie

Usage
------------

	Usage: smspie 0851234567

	Send SMS via command line

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -C PROVIDER, --provider=PROVIDER
		                sets the SMS provider
	  -c CONFIG, --config=CONFIG
		                sets the path to the config file
	  -i, --import-contacts
		                import Meteor contacts, copy and paste into the config
		                file
	  -l, --list            list the people in your phonebook
	  -m MESSAGE, --message=MESSAGE
		                the message you want to send
	  -u USERNAME, --username=USERNAME
		                set your username
	  -p PASSWORD, --password=PASSWORD
		                set your password
	  -v, --verbose         set the output as verbose (debug)


Installation
------------

### Global

To install run this as root: `python setup.py install`

### Local

If you've never setup a local install before run `mkdir -p ~/lib/python/`

Then add to your shellrc or change you environment with `export PYTHONPATH=$HOME/lib/python/`

Now do a local install do: `python setup.py install --home="$HOME"`

Examples
------------
Importing contacts for your phonebook

	$ smspie -C meteor --import-contacts
	Add the following to the ~/.smspie/config.yaml under the section phonebook

	phonebook:
	- {phonenumber: 0851234567, username: John}
	- {phonenumber: 0851234567, username: Smith}

Sending a message to a person in your phonebook

	$ smspie -C meteor John
	[ Using a session for 0851234567@meteor ... ]
	[ Recipient: John (0851234567) ]
	> oh hi, lets met up later.
	> 
	[ Message sent to John (0851234567) ]

Sending a message to a number

	$ smspie -C meteor 0851234567
	[ Using a session for 0851234567@meteor ... ]
	[ Recipient:  (0851234567) ]
	> oh hi, lets met up later.
	> 
	[ Message sent to  (0851234567) ]

Listing the contacts you have

	$ smspie -l
	John          0851234567
	Smith         0851234567

Extra
------------
Something extra you might like to do is alias the commands, as mentioning what
section your provider is from is tedious. So `alias meteorsms="smspie -C meteor"`
can save you time, and can also be handy for multiple-user systems.
