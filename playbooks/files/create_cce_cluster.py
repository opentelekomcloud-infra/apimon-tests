#!/usr/bin/env python3
import sys
import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

cluster_name = sys.argv[1]
router_name = sys.argv[2]
network_name = sys.argv[3]

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

router_id = conn.network.find_router(router_name).id
network_id = conn.network.find_network(network_name).id

clusterparam = {
        'name': cluster_name,
        'spec': {
                'type': 'VirtualMachine',
                'hostNetwork': {
                        'vpc': router_id,
                        'subnet': network_id
                },
                'flavor': 'cce.s1.small',
                'containerNetwork': {
                        'mode': 'overlay_l2',
                        'cidr': '172.16.0.0/16'
                }
        }
}


cluster = conn.cce.create_cluster(**clusterparam)
conn.cce.wait_for_cluster(cluster, wait=1200)
#TBD wait_for_job_completion()






