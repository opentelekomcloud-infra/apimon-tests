#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

volumes = list(conn.block_storage.volumes(name=sys.argv[1]))
volume_id = volumes[0].id
snapshots = list(conn.block_storage.snapshots(name=sys.argv[2]))
snapshot_id = snapshots[0].id


backup = conn.block_storage.create_backup(volume_id=volume_id,
                                          snapshot_id=snapshot_id,
                                          name=sys.argv[3])

conn.block_storage.wait_for_status(backup,
                                   status='available',
                                   wait=1200)
