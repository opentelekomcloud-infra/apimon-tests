#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()
sdk.register_otc_extensions(conn)
# openstack.enable_logging(debug=True, http_debug=True)

container_name = sys.argv[1]

# delete container
conn.obs.delete_container(container_name, ignore_missing=True)
