#!/usr/bin/env python

"""
Dynect API SOAP Examples

Logs into the API, gets a session token, creates a brand new Geo Service
that is NOT linked to any nodes, updates a Geo Service, and then logs out.

"""

import suds.client
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

CUST = ''
USER = ''
PASS = ''

# The path to the Dynect API WSDL file
base_url = 'https://api2.dynect.net/wsdl/current/Dynect.wsdl'

# Create a client instance
client = suds.client.Client(base_url)

# Logging in
response = client.service.SessionLogin(
    customer_name = CUST,
    user_name = USER,
    password = PASS,
    fault_incompat = 1,
)

if response.status != 'success':
    print ("Login request failed!")
    pp.pprint(response)
    raise SystemExit

token = response.data.token

print ("Token: %s" % token)

"""

CreateGeo

To create a Geo service, one must specify a unique
name and define at least one Geo Region Group.

A Geo Region Group consists of a unique name, a
list of countries that the group represents, and
rdata that will be served.

"""

response = client.service.CreateGeo(
	name = 'test geo',
	groups = [{
		'name' : 'test group',
		'countries' : ['US'],
		'rdata' : {
			'a_rdata':[{
				'address':'9.9.9.9'
			}]
		}
	}],
	token = token,
	fault_incompat = 1,
)

print "Response: %s" % pp.pformat(response)

if response.status != 'success':
    print "Record request failed!"
    pp.pprint(response)
    raise SystemExit

"""

UpdateGeo

To update a Geo service, one must identify it using
the name specified at the time of creation.

Only the fields specified are updated. For example, if
a node is to be linked to the Geo Service, `Groups` 
do not need to be specified.

"""

response = client.service.UpdateGeo(
	name = 'test geo',
	nodes = {
		'fqdn' : 'blat.bitesnbits.co',
		'zone' : 'bitesnbits.co',
	},
	token = token,
	fault_incompat = 1,
)

print "Response: %s" % pp.pformat(response)

if response.status != 'success':
    print "Record request failed!"
    pp.pprint(response)
    raise SystemExit

response = client.service.SessionLogout(
    token = token,
    fault_incompat = 1,
)

if response.status != 'success':
    print "Logout request failed!"
    pp.pprint(response)
    raise SystemExit

print "Successfully logged out"