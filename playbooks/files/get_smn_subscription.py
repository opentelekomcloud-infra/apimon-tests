#!/usr/bin/env python3

import openstack
import sys
import json

from otcextensions import sdk

conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]

conn.smn.subscriptions(topic_urn)
