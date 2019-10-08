#!/usr/bin/env python3

import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

clusters = conn.cce.clusters()
for cluster in clusters:
   print(cluster)
#cluster = conn.cce.find_cluster('cee67c33-c024-11e9-8b88-0255ac101618')
#print(cluster.status["status"])
#cluster_status = conn.cce.wait_for_cluster(cluster)
#print(cluster_status)
