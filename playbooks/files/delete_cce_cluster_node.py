#!/usr/bin/env python3

import sys
import time

import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

cluster = conn.cce.find_cluster(sys.argv[1])
node = conn.cce.find_cluster_node(cluster, sys.argv[2])

if cluster and node:
  node = conn.cce.delete_cluster_node(cluster, node)
  time.sleep(90)