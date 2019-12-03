#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)

id = '08435fb2-b47c-4128-8a14-ee48f30ab585'

response = conn.nat.get_dnat_rule(id)
print(response)
