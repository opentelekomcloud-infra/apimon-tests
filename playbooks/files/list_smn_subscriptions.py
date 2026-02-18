#!/usr/bin/env python3

import openstack
import json

from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()

sdk.register_otc_extensions(conn)

#list(conn.smn.topics())

#print(list)

list_subscriptions = list(conn.smn.subscriptions())

output = [sub.to_dict() for sub in list_subscriptions]

print(json.dumps(output))
