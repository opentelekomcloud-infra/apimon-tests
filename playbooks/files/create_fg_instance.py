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

attrs = {
    "func_name": instance_name,
    'package': 'default',
    'runtime': 'Python3.9',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'zip',
}

fg = conn.functiongraph.create_function(**attrs)
