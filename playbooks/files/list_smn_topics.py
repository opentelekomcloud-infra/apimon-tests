#!/usr/bin/env python3

import openstack

import sys
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

#topic = list(conn.smn.topics())
#templates = list(conn.smn.templates())

# Retrieve topics
topics = list(conn.smn.topics())

# Print results
for t in topics:
    print(f"{t.id}  {t.name}")

