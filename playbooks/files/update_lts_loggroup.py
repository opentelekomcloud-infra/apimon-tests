#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

conn = openstack.connect()
sdk.register_otc_extensions(conn)

lg_id = sys.argv[1]

attrs = {
    'ttl_in_days': 2
}
log_group = conn.lts.update_group(group=lg_id, **attrs)
