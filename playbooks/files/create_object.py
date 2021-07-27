#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()
# openstack.enable_logging(debug=True, http_debug=True)

container_name = sys.argv[1]
object_name = sys.argv[2]

# create object
conn.obs.create_object(container_name, name=object_name)
