#!/usr/bin/env python3

import openstack

# openstack.enable_logging(debug=True, http_debug=True)

conn = openstack.connect()

list(conn.block_storage.backups())
