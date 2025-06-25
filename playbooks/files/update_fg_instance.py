#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

instance_name = sys.argv[1]
conn = openstack.connect()
sdk.register_otc_extensions(conn)

#for fgs in conn.function_graph.functions():
#    print(fgs)

#for fgs in conn.function_graph.functions():
#    if fgs["func_name"] == instance_name:
#      urn = fgs["func_urn"]


#print(urn)

func_attrs = {
    'func_name': instance_name,
    'package': 'default',
    'runtime': 'Node.js14.18',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'zip',
}

fg = conn.functiongraph.create_function(**func_attrs)

alias_attrs = {
    'name': 'a1',
    'version': 'latest'
}
alias = conn.functiongraph.create_alias(fg.func_urn, **alias_attrs)

new_attrs = {
    'version': 'latest',
    'description': 'apimon-description-update',
}
updated = conn.functiongraph.update_alias(fg, alias, **new_attrs)
