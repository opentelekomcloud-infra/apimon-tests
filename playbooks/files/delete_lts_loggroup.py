#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()
lg_id = sys.argv[1]
log_group = conn.lts.delete_group(group=lg_id)
