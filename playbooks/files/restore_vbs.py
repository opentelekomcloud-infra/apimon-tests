#!/usr/bin/env python3

import openstack
import sys
from urllib.parse import urljoin

# ----------------------------------------------------------------------
# Authenticate via OpenStack SDK (Keystone)
# ----------------------------------------------------------------------

conn = openstack.connect()

if len(sys.argv) < 2:
    print("Usage: restore.py <backup_name> [<new_volume_name>]")
    sys.exit(1)

backup_name = sys.argv[1]
new_name = sys.argv[2] if len(sys.argv) > 2 else None

# Find the backup
backups = list(conn.block_storage.backups(details=True))
backup = next((b for b in backups if b.name == backup_name), None)

if not backup:
    print(f"Backup '{backup_name}' not found")
    sys.exit(1)

backup_id = backup.id
volume_id = backup.volume_id

print(f"Found backup {backup_id} for volume {volume_id}")

# ----------------------------------------------------------------------
# VBS vendor API endpoint discovery
# ----------------------------------------------------------------------

# We look up the "evs" service endpoint from the Keystone catalog.
vbs_service = conn.session.get_endpoint(
    interface="public",
    service_type="vbs"
)

if not vbs_service:
    print("ERROR: Could not find VBS endpoint in service catalog.")
    sys.exit(1)

print(f"VBS endpoint: {vbs_service}")

# Keystone token from OpenStack session
token = conn.session.get_token()

# ----------------------------------------------------------------------
# Trigger VBS restore via vendor API (returns job_id)
# ----------------------------------------------------------------------

restore_url = urljoin(
    vbs_service,
    f"/v2/{conn.current_project_id}/cloudbackups/{backup_id}/restore"
    )

payload = {
    "restore": {
        "volume_id": volume_id
    }
}

# Optional new name
if new_name:
    payload["restore"]["name"] = new_name

headers = {
    "Accept": "application/json",
}

print(f"Requesting restore from VBS vendor API: {restore_url}")

resp = conn.session.post(restore_url, json=payload, headers=headers)
resp.raise_for_status()

data = resp.json()
job_id = data.get("job_id")

if not job_id:
    print("ERROR: VBS restore did not return job_id. Response:")
    print(resp.text)
    sys.exit(1)

print(f"job_id = {job_id}")
