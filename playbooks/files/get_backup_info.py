#!/usr/bin/env python3

import openstack
import json
import sys

conn = openstack.connect()

if len(sys.argv) > 1:
    query = sys.argv[1]
    for backup in conn.block_storage.backups():
        if backup.name == query or backup.id == query:
            print(json.dumps(backup.to_dict()))
            exit(0)
