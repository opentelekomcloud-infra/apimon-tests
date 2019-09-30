#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.image.get('')

conn.image.get('https://ims.eu-de.otc.t-systems.com')
