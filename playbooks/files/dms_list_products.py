#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()
sdk.register_otc_extensions(conn)

spec = sys.argv[1]
for raw in conn.dms.products():
    if raw.spec_code == spec:
        print(raw.storage)
        print(raw.product_id)
        print(raw.io[0].get("storage_spec_code"))
        break
