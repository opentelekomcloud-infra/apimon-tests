#!/usr/bin/env python3

import openstack

import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

#topic = list(conn.smn.topics())
#templates = list(conn.smn.templates())

topic_urn = sys.argv[1]

topic = conn.smn.delete_topic(topic_urn)

print(topic)
