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
internal_service_port = 8080
external_service_port = 80
#port_id = '89d9d23f-9173-4522-b6ed-a4fe0c3ddb26'
private_ip = '192.168.3.3'
protocol = 'TCP'


response = conn.nat.create_dnat_rule(nat_gateway_id=nat_gateway_id,
    floating_ip_id=floating_ip_id, internal_service_port=internal_service_port,
    external_service_port=external_service_port, private_ip=private_ip, protocol=protocol)
print(response)
