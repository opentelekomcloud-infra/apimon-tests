#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)

id = '21efd44f-0f2c-4398-9e00-4f10010ecd76'

response = conn.nat.delete_dnat_rule(id=id)
print(response)
