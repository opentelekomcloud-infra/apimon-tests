#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()
sdk.register_otc_extensions(conn)

# openstack.enable_logging(debug=True, http_debug=True)

container_name = sys.argv[1]
object_name = sys.argv[2]

# create object
conn.obs.create_object(container=container_name, name=object_name)
