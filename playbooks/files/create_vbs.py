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

volume_id = sys.argv[1]
backup_name = sys.argv[2]

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
# Trigger VBS backup via vendor API (returns job_id)
# ----------------------------------------------------------------------

create_vbs_url = urljoin(
    vbs_service,
    f"/v2/{conn.current_project_id}/cloudbackups"
    )

payload = {
    "backup": {
        "volume_id": volume_id,
        "name": backup_name
    }
}

headers = {
    "Accept": "application/json",
}

print(f"Creating VBS backup vendor API: {create_vbs_url}")

resp = conn.session.post(create_vbs_url, json=payload, headers=headers)
resp.raise_for_status()

data = resp.json()
job_id = data.get("job_id")

if not job_id:
    print("ERROR: VBS backup did not return job_id. Response:")
    print(resp.text)
    sys.exit(1)

print(f"job_id = {job_id}")
