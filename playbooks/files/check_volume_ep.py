#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.volume.get('')

conn.volume.get('https://evs.eu-de.otc.t-systems.com')
