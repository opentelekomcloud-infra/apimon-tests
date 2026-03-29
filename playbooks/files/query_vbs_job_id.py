#!/usr/bin/env python3

import openstack
import sys
from urllib.parse import urljoin

# ----------------------------------------------------------------------
# Authenticate via OpenStack SDK (Keystone)
# ----------------------------------------------------------------------

conn = openstack.connect()

if len(sys.argv) < 2:
    sys.exit(1)

job_id = sys.argv[1]

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

# Keystone token from OpenStack session
token = conn.session.get_token()

# ----------------------------------------------------------------------
# Poll asynchronous job status
# ----------------------------------------------------------------------

job_url = urljoin(vbs_service, f"/v1/{conn.current_project_id}/jobs/{job_id}")

poll_headers = {"Accept": "application/json"}

jresp = conn.session.get(job_url, headers=poll_headers)
jresp.raise_for_status()
job_info = jresp.json()

status = job_info.get("status")

print(f"Job {job_id} status: {status}")
