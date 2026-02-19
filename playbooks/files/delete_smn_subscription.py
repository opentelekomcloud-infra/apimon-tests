#!/usr/bin/env python3

import openstack
import sys

from otcextensions import sdk

conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_subscription = sys.argv[1]

conn.smn.delete_subscription(topic_subscription)
