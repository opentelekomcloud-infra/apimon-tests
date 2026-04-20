#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk

instance_name = sys.argv[1]
timer_name = instance_name
conn = openstack.connect()
sdk.register_otc_extensions(conn)

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

trigger = conn.functiongraph.create_trigger(fg, **trigger_attrs)
