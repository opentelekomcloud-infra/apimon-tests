#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)


cluster = conn.cce.find_cluster(sys.argv[1])
conn.cce.wait_for_cluster(cluster)
