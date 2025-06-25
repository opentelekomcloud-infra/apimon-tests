#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

instance_name = sys.argv[1]

for fgs in conn.function_graph.functions():
    if fgs["func_name"] == instance_name:
      urn_for_deletion = fgs["func_urn"]


print(urn_for_deletion)

attrs = {
    'func_urn': urn_for_deletion + ":" + instance_name ,
}

fg = conn.functiongraph.delete_function(function=attrs)
