#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

instance_name = sys.argv[1]
timer_name = instance_name
conn = openstack.connect()
sdk.register_otc_extensions(conn)

#for fgs in conn.function_graph.functions():
#    print(fgs)

#for fgs in conn.function_graph.functions():
#    if fgs["func_name"] == instance_name:
#      urn = fgs["func_urn"]


#print(urn)

trigger_attrs = {
            "trigger_type_code": "TIMER",
            "trigger_status": "ACTIVE",
            "event_data": {
                "name": "Timer-" + timer_name,
                "schedule": "1m",
                "schedule_type": "Rate"
            }
        }

func_attrs = {
    'func_name': instance_name,
    'package': 'default',
    'runtime': 'Python3.9',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'zip',
}

fg = conn.functiongraph.create_function(**func_attrs)

#print(fg)

trigger = conn.functiongraph.create_trigger(fg, **trigger_attrs)

#func_urn = fg(func_urn)
#print(func_urn)


#inv = conn.functiongraph.executing_function_asynchronously(func_urn, attrs={'a': 'b'})
