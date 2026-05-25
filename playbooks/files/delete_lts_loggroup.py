#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

conn = openstack.connect()
sdk.register_otc_extensions(conn)

lg_id = sys.argv[1]
log_group = conn.lts.delete_group(group=lg_id)
