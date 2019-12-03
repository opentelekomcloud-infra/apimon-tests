#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)

id = '66bfee0f-eb3d-46ec-8c9b-c9f7ba92f242'

response = conn.nat.delete_snat_rule(id=id)
print(response)
