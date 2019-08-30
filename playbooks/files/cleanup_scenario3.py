#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

# Script must get 2 prefix for object to cleanup
name_contains = sys.argv[1]

if not name_contains:
    sys.exit(1)

for res in conn.block_storage.backups():
    if name_contains in res.name:
        conn.block_storage.delete_backup(res.id)
        conn.block_storage.wait_for_delete(res, timeout=300)

# for res in conn.block_storage.snapshots():
#     if name_contains in res.name:
#         conn.block_storage.delete_snapshot(res.id)
#         conn.block_storage.wait_for_delete(res)

for res in conn.block_storage.volumes():
    if name_contains in res.name:
        conn.block_storage.delete_volume(res.id)
        conn.block_storage.wait_for_delete(res)
