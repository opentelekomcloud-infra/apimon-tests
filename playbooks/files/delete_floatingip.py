#!/usr/bin/env python3

import openstack
import sys

# openstack.enable_logging(debug=True, http_debug=True)

fipid = sys.argv[1]

conn = openstack.connect()

conn.network.delete_ip(fipid)
