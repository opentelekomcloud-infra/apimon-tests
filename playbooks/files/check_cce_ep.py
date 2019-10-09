#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(debug=True)

conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

conn.cce.get('')

conn.cce.get('https://cce.eu-de.otc.t-systems.com')
