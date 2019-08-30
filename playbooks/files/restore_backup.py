#!/usr/bin/env python3

import openstack
import logging
import sys

#openstack.enable_logging(debug=True, http_debug=True)

conn = openstack.connect()
#Until ES150 is completed this query can be done only in old way
#backups = list(conn.block_storage.backups(name=sys.argv[1]))
backups = list(conn.block_storage.backups())
backup = [detail for detail in backups if detail.name == sys.argv[1]]
backup =  next(iter(backup),None)
backup_id = backup.id
volume_id = backup.volume_id

backup = conn.block_storage.restore_backup(backup_id, volume_id, name=sys.argv[2])
conn.block_storage.wait_for_status(backup,status='available')


