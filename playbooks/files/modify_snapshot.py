#!/usr/bin/env python3

import openstack
import logging
import sys

#openstack.enable_logging(debug=True, http_debug=True)

conn = openstack.connect()
snapshots = list(conn.block_storage.snapshots(name=sys.argv[1]))
snapshot_id = snapshots[0].id

snapshot = conn.block_storage.put(
    '/snapshots/'+snapshot_id,
    json={
        "snapshot": {
        "name": sys.argv[2]
    }
    }
)
