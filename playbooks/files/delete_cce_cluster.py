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

timer = 0

if cluster:
  conn.cce.delete_cluster(cluster)
  while cluster is not None:
    cluster = conn.cce.find_cluster(sys.argv[1])
    if timer > 300:
      print("Cluster run out if time")
      break
    elif cluster is None:
      print("Cluster has been deleted")
      break
    timer = timer + 5
    print("Current time in seconds: " + timer)
  



