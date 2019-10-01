#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.orchestration.get('')

conn.orchestration.get('https://rts.eu-de.otc.t-systems.com')
