#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.network.get('')

conn.network.get('https://vpc.eu-de.otc.t-systems.com')
