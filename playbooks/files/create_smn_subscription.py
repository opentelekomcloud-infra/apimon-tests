#!/usr/bin/env python3

import openstack
import sys

from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]

attrs = {

      "endpoint": "user@example.com",
      "protocol": "email",
      "remark": "Lorem"
}

result = conn.smn.create_subscription(topic_urn, **attrs)

print(result.id)
