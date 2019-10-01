#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.identity.get('')

conn.identity.get('https://iam.eu-de.otc.t-systems.com')
