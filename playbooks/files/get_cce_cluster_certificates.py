#!/usr/bin/env python3
import sys
import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

cluster_name = sys.argv[1]

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

#find cce cluster
cluster = conn.cce.find_cluster(cluster_name)

#get cce cluster certificates
certificates = conn.cce.get_cluster_certificates(cluster)






