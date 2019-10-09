#!/usr/bin/env python3
import sys
import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

cluster_name = sys.argv[1]
cluster_node_name = sys.argv[2]

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

#find cce cluster
cluster = conn.cce.find_cluster(cluster_name)

#find cce cluster node
cluster_node = conn.cce.find_cluster_node(cluster, cluster_node_name)

#query cce cluster node
conn.cce.get_cluster_node(cluster, cluster_node)

