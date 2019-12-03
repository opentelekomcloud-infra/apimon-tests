#!/usr/bin/env python3
import sys

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)
spec = '2'
id = sys.argv[1]

print(id)


gateway = conn.nat.get_gateway(id)
if gateway is None:
    print("No gateway found!")
else:
    conn.nat.update_gateway(gateway, spec=spec)
