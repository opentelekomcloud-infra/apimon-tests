#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

obs_bucket = sys.argv[1]

attrs = {
    "bucket_name": obs_bucket,
    "file_prefix_name": "file-apimon-",
    "lts": {
        "is_lts_enabled": True
    },
    "status": "enabled",
    "tracker_name": "system",
    "detail": ""
}

tracker = conn.cts.create_tracker(**attrs)
