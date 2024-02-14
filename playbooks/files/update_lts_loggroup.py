#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

lg_id = sys.argv[1]

attrs = {
    'ttl_in_days': 2
}
log_group = conn.lts.update_group(group=lg_id, **attrs)
