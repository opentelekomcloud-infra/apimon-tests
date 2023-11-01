#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()
# openstack.enable_logging(debug=True, http_debug=True)

container_name = sys.argv[1]
object_name = sys.argv[2]

# get object
conn.object_store.get_object(object_name, container=container_name)
