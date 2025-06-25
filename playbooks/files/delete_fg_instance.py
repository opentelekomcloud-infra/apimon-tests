#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

#for fgs in conn.function_graph.functions():
#    print(fgs)

instance_name = sys.argv[1]
#instance_name = "FGTest1"
#vpc_id = sys.argv[2]
#subnet_id = sys.argv[3]
#sg_id = sys.argv[4]
#inst_pw = sys.argv[5]
#az_name = sys.argv[6]

for fgs in conn.function_graph.functions():
    if fgs["func_name"] == instance_name:
      urn_for_deletion = fgs["func_urn"]


print(urn_for_deletion)

attrs = {
    'func_urn': urn_for_deletion + ":" + instance_name ,
}

fg = conn.functiongraph.delete_function(function=attrs)
