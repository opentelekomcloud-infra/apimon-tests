#!/usr/bin/env python3

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
#sdk.register_otc_extensions(conn)

nat_gateway_id = '11cc6ee1-ae79-4d6d-a0a8-97aafcea3aa3'
floating_ip_id = '78b7c30b-180d-49e1-b212-03e2c39698f4'
network_id = 'ad7b92c2-9f55-4ddf-90b0-8a1c98d21b21'

response = conn.nat.create_snat_rule(nat_gateway_id=nat_gateway_id, floating_ip_id=floating_ip_id, network_id=network_id)
print(response)
