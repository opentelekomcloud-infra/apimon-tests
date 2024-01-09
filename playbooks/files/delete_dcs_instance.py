#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

instance_name = sys.argv[1]
instance = conn.dcs.find_instance(instance_name)

id = (instance.id)
conn.dcs.delete_instance(id)

