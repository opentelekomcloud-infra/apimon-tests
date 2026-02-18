#!/usr/bin/env python3

import openstack
import sys
import json

from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]

# result=conn.smn.subscriptions(topic_urn)

# print(result)


list_topic_subscriptions = list(conn.smn.subscriptions(topic_urn))

output = [sub.to_dict() for sub in list_topic_subscriptions]

print(json.dumps(output))