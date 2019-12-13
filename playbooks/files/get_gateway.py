#!/usr/bin/env python3

import openstack
import sys

openstack.enable_logging(True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()


id = sys.argv[1]

gateway = conn.nat.get_gateway(id)
print(gateway)
