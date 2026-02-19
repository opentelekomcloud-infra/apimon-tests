#!/usr/bin/env python3

import openstack

import sys
from otcextensions import sdk

conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]

result = conn.smn.get_topic(topic_urn)

print(result)
