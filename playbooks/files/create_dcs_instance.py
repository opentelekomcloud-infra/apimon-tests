#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

instance_name = sys.argv[1]
vpc_id = sys.argv[2]
subnet_id = sys.argv[3]
sg_id = sys.argv[4]
inst_pw = sys.argv[5]
az_name = sys.argv[6]

attrs = {
    "name": instance_name,
    "engine": "Redis",
    "capacity": 2,
    "resource_spec_code": "dcs.single_node",
    "engine_version": "3.0",
    "vpc_id": vpc_id,
    "product_id": "OTC_DCS_SINGLE",
    "password": inst_pw,
    "maintain_begin": "02:00:00",
    "maintain_end": "06:00:00",
    "available_zones": [
        az_name
    ],
    "subnet_id": subnet_id,
    "security_group_id": sg_id
}

instance = conn.dcs.create_instance(**attrs)
