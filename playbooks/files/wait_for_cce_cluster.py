#!/usr/bin/env python3

import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)


cluster = conn.cce.get_cluster('d6f48aa6-cd8b-11e9-a4c3-0255ac101617')
#print(cluster)
conn.cce.wait_for_cluster(cluster)
