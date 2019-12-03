#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)

id = 'c545ccdf-05ff-4157-a1e2-cd6b79863827'

gateway = conn.nat.get_gateway(id)
print(gateway)
