#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

cluster = conn.cce.find_cluster(sys.argv[1])
dict = {
    'metadata': {
        'name': sys.argv[1]
    },
    'spec': {
        'type': 'VirtualMachine',
        'version': 'v1.11.3-r1',
        'hostNetwork': {
            'vpc': sys.argv[2],
            'subnet': sys.argv[3]
        },
        'flavor': 'cce.s1.small',
        'containerNetwork': {
            'mode': 'overlay_l2',
            'cidr': '172.16.0.0/16'
        }
    }
}

if (cluster is None):
  cluster = conn.cce.create_cluster(**dict)
  #conn.cce.wait_for_cluster(cluster)
