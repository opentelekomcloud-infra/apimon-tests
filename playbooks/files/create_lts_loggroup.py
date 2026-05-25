#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

conn = openstack.connect()
sdk.register_otc_extensions(conn)

lg_name = sys.argv[1]

attrs = {
    'log_group_name': lg_name,
    'ttl_in_days': 6
}
log_group = conn.lts.create_group(**attrs)

print(log_group["log_group_id"])
