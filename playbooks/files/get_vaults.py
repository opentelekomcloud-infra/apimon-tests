#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk


conn = openstack.connect()
sdk.register_otc_extensions(conn)

# openstack.enable_logging(True)

vault_id = sys.argv[1]
vault = conn.cbr.get_vault(vault=vault_id)
print(vault)
