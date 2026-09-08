#!/usr/bin/env python3

import openstack
from otcextensions import sdk

# openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)


cluster = conn.cce.get_cluster('e9d8539e-c894-11e9-a4c3-0255ac101618')
