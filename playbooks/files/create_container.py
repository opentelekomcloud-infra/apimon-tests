#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()
# openstack.enable_logging(debug=True, http_debug=True)

container_name = sys.argv[1]

# create container
headers = {'x-amz-acl': 'public-read'}
conn.obs.create_container(name=container_name, headers=headers)
