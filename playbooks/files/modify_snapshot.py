#!/usr/bin/env python3

import openstack
import sys

# openstack.enable_logging(debug=True, http_debug=True)

conn = openstack.connect()
snapshot_id = sys.argv[1]

snapshot = conn.block_storage.put(
    '/snapshots/'+snapshot_id,
    json={
        "snapshot": {
          "name": sys.argv[2]
          }
    }
)
