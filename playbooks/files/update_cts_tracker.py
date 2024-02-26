#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

obs_bucket = sys.argv[1]

attrs = {
    "bucket_name": obs_bucket,
    "status": "disabled"
}

tracker_name = "system"
conn.cts.update_tracker(tracker_name, **attrs)
