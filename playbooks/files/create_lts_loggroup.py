#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

lg_name = sys.argv[1]

attrs = {
    'log_group_name': lg_name,
    'ttl_in_days': 6
}
log_group = conn.lts.create_group(**attrs)

print(log_group["log_group_id"])
