#!/usr/bin/env python3

import openstack

openstack.enable_logging(debug=True)

conn = openstack.connect()

conn.compute.get('')

conn.compute.get('https://ecs.eu-de.otc.t-systems.com')
