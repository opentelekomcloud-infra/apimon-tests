#!/usr/bin/env python3
import sys
import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

#list cce clusters
list(conn.cce.clusters())






