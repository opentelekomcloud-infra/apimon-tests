#!/usr/bin/env python3

import openstack
import sys

from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]
display_name = sys.argv[2]

attrs = {
    'display_name': display_name
}

conn.smn.update_topic(topic_urn, **attrs)