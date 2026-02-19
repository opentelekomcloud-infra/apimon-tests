#!/usr/bin/env python3

import openstack
import sys

from otcextensions import sdk

conn = openstack.connect()

sdk.register_otc_extensions(conn)

topic_urn = sys.argv[1]

policy = {
    "Version": "2016-09-07",
    "Id": "__default_policy_ID",
    "Statement": [
        {
            "Sid": "__service_pub_0",
            "Effect": "Allow",
            "Principal": {
                "Service": ["obs"]
            },
            "Action": ["SMN:Publish", "SMN:QueryTopicDetail"],
            "Resource": topic_urn
        }
    ]
}


attrs = {
    "value": policy
}

conn.smn.topic_attributes(topic_urn, name="access_policy", **attrs)
