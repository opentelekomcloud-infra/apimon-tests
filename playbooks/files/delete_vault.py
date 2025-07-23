#!/usr/bin/env python3

import sys
import openstack
from otcextensions import sdk


conn = openstack.connect()
sdk.register_otc_extensions(conn)

# openstack.enable_logging(True)
name = sys.argv[1]
for vault in conn.cbr.vaults(name=name):
    conn.cbr.delete_vault(vault=vault)
