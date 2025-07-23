#!/usr/bin/env python3

import openstack
from otcextensions import sdk


conn = openstack.connect()
sdk.register_otc_extensions(conn)

# openstack.enable_logging(True)

for vault in conn.cbr.vaults():
    print(vault)
