#!/usr/bin/env python3
import sys
import time
import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)
cluster_name = sys.argv[1]
cluster_node_name = sys.argv[2]

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

cluster = conn.cce.find_cluster(cluster_name)
clusternode = conn.cce.find_cluster_node(cluster, cluster_node_name)
conn.cce.delete_cluster_node(cluster, clusternode)

time.sleep(180)
#TBD wait for delete
#conn.cce.wait_for_delete(clusternode,interval=60)
#wait_for_job_completion()
