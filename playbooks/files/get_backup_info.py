#!/usr/bin/env python3

import openstack
import json
import sys

conn = openstack.connect()

if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    query = None
try:
    print(json.dumps(conn.block_storage.get_backup(query).to_dict()))
except:
    for backup in conn.block_storage.backups():
        if query and backup.name == query:
            print(json.dumps(backup.to_dict()))
        elif not query:
            print(json.dumps(backup.to_dict()))
exit(0)
