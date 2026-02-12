#!/usr/bin/env python3

import openstack

import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_name = sys.argv[1]

attrs = {
    'name': topic_name
}

result = conn.smn.create_topic(**attrs)

print(result.id)
