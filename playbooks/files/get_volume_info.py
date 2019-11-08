#!/usr/bin/env python3

import openstack
import json
import sys

conn = openstack.connect()

if len(sys.argv) > 1:
    query = sys.argv[1]
    for vol in conn.block_storage.volumes():
        if vol.id == query or vol.name == query:
            print(json.dumps(vol.to_dict()))
            exit(0)
