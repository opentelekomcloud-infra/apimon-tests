#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

instance_name = sys.argv[1]

attrs = {
    "description": "APImon - description of DCS instance changed"
}

instance = conn.dcs.find_instance(instance_name)
conn.dcs.update_instance(instance, **attrs)
